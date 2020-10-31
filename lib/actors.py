"""The module contains a number of actors to be executed by a schedule. The
actors provide some necessary operations with the Snake-Server such as
screenshot generation and so on.
"""

import logging
from typing import Tuple, Dict, List
from pathlib import Path

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq.rate_limits import RateLimiterBackend
from dramatiq.results.backends import (
    RedisBackend as ResultRedisBackend,
    StubBackend as ResultStubBackend,
)
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import (
    RedisBackend as RateLimitsRedisBackend,
    StubBackend as RateLimitsStubBackend,
)
from dramatiq.results import Results, ResultBackend
from dramatiq.middleware import Prometheus
import telegram

from lib import settings
from lib import funcs
from lib.parse import ParseError
from lib.api import APIError


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

rate_limits_backend: RateLimiterBackend
broker: dramatiq.Broker
result_backend: ResultBackend

if settings.UNIT_TESTS:
    # Setup backends
    result_backend = ResultStubBackend()
    rate_limits_backend = RateLimitsStubBackend()
    # Setup brokers
    broker = StubBroker()
else:
    logger.info("Setup redis broker")
    # Setup backends
    result_backend = ResultRedisBackend(url=settings.RESULT_REDIS_URL)
    rate_limits_backend = RateLimitsRedisBackend(
        url=settings.RATE_LIMITS_REDIS_URL)
    # Setup brokers
    broker = RedisBroker(url=settings.BROKER_REDIS_URL)

results = Results(backend=result_backend)
broker.add_middleware(results)

if settings.PROMETHEUS_METRICS_SERVER_ENABLE:
    broker.add_middleware(Prometheus(
        http_host=settings.PROMETHEUS_METRICS_LISTEN_HOST,
        http_port=settings.PROMETHEUS_METRICS_LISTEN_PORT,
    ))

dramatiq.set_broker(broker=broker)


DISTRIBUTED_MUTEX_REPORT = ConcurrentRateLimiter(rate_limits_backend,
                                                 "distributed-mutex-report",
                                                 limit=1)

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


@dramatiq.actor(max_retries=0, store_results=True)
def dispatch_taking_screenshots() -> Dict[int, List[str]]:
    """Checks games on a specified in settings server and dispatches group of
    tasks for taking screenshots

    Returns:
      A dictionary in which keys are game identifiers and values are lists
      of screenshot files
    """
    logger.debug('Dispatching taking games screenshots tasks')
    try:
        group = dramatiq.group(take_sized_screenshots_by_game_id.message(
            game_id) for game_id in funcs.get_games_ids())
        group.run()
        # Dictionary to collect game identifiers as keys and screenshot file
        # name lists as values for report
        games_screenshots = {}
        for game_id, files in group.get_results(block=True):
            if files:
                logger.debug("Game %s => %s", game_id, files)
                games_screenshots[game_id] = files
        return games_screenshots
    except ParseError as e:
        logger.error('Parse error: %s', e)
    except APIError as e:
        logger.error('API response error: %s', e)
    return {}


@dramatiq.actor(max_retries=0, store_results=True)
def take_sized_screenshots_by_game_id(game_id: int) -> Tuple[int, list]:
    """Takes screenshots with regards to required sizes which are specified in
    settings.

    Parameters:
      game_id: a game identifier

    Returns:
      A tuple with a game identifier and a list of screenshot files
    """
    logger.debug('Taking screenshots: %s', game_id)
    try:
        files = funcs.take_sized_screenshots_by_game_id(game_id)
        return game_id, files
    except ParseError as e:
        logger.error('Parse error: %s', e)
    except APIError as e:
        logger.error('API response error: %s', e)
    return game_id, []


@dramatiq.actor(max_retries=5)
def write_games_screenshots_json_report(
        games_screenshots: Dict[int, List[str]]):
    """Writes a JSON report with given data. The output file name is specified
    in settings

    Parameters:
      games_screenshots: a data to be written as a report
    """
    if games_screenshots:
        logger.debug('Report games: %s', games_screenshots)
    with DISTRIBUTED_MUTEX_REPORT.acquire():
        funcs.write_games_screenshots_json_report(games_screenshots)


@dramatiq.actor(max_retries=1)
def delete_expired_screenshots_cache():
    """Deletes expired screenshot cache
    """
    exclude_screenshots: tuple
    with DISTRIBUTED_MUTEX_REPORT.acquire():
        exclude_screenshots = funcs.get_latest_screenshots_file_names()

    funcs.delete_screenshots(exclude_screenshots)


@dramatiq.actor(max_retries=5)
def send_games_list_to_telegram(chat_id, *args):
    """Sends a message with a list of games in to a specific chat
    """
    games = funcs.sort_games(funcs.get_games())

    game_lines = []
    for game in games:
        game_lines.append(
            f'\\* _game {game.name}_ `{game.count}/{game.limit}` /show\\_{game.id}')

    # TODO: Move the code to the funcs module.
    # TODO: Add emoji.
    text = f'*Games*\n\n' + '\n'.join(game_lines)

    bot.send_message(
        chat_id=chat_id,
        parse_mode=telegram.parsemode.ParseMode.MARKDOWN_V2,
        text=text,
    )


@dramatiq.actor(max_retries=5)
def send_game_to_telegram(chat_id, game_id):
    """Sends a message with a list of games in to a specific chat
    """
    game = funcs.get_game(game_id)

    # TODO: Move the code to the funcs module.
    # TODO: Add emoji.
    text = f'*Game {game.name}*\n\n' \
           f'_Players_: `{game.count}/{game.limit}`\n' \
           f'_Size_: `{game.width}x{game.height}`\n' \
           f'_Rate_: `{game.rate}pps`\n\n' \
           f'[Play now\\!]({funcs.get_game_link(game)})\n\n' \
           f'Back /list'

    image_path = funcs.get_image_path(game_id,
                                      (game.width, game.height),
                                      settings.SCREENSHOT_SLUG_MEDIUM)
    if Path(image_path).is_file():
        bot.send_photo(
            chat_id=chat_id,
            photo=open(image_path, 'rb'),
            caption=text,
            parse_mode=telegram.parsemode.ParseMode.MARKDOWN_V2,
        )
    else:
        bot.send_message(
            chat_id=chat_id,
            parse_mode=telegram.parsemode.ParseMode.MARKDOWN_V2,
            text=text,
            disable_web_page_preview='True',
        )
