"""The module contains a number of actors to be executed by a schedule. The actors
provide some necessary operations with the Snake-Server such as screenshot generation
and so on.
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import logging

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq.results.backends import (
    RedisBackend as ResultRedisBackend,
    StubBackend as ResultStubBackend,
)
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import (
    RedisBackend as RateLimitsRedisBackend,
    StubBackend as RateLimitsStubBackend,
)
from dramatiq.results import Results

from lib import settings
from lib import funcs
from lib.parse import ParseError
from lib.api import APIError


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


if settings.UNIT_TESTS:
    # Setup backends
    result_backend = ResultStubBackend()
    rate_limits_backend = RateLimitsStubBackend()
    # Setup brokers
    broker = StubBroker()
    broker.add_middleware(Results(backend=result_backend))
    dramatiq.set_broker(broker)
else:
    logger.info("Setup redis broker")
    # Setup backends
    result_backend = ResultRedisBackend(url=settings.RESULT_REDIS_URL)
    rate_limits_backend = RateLimitsRedisBackend(url=settings.RATE_LIMITS_REDIS_URL)
    # Setup brokers
    broker = RedisBroker(url=settings.BROKER_REDIS_URL)
    broker.add_middleware(Results(backend=result_backend))
    dramatiq.set_broker(broker=broker)


DISTRIBUTED_MUTEX_REPORT = ConcurrentRateLimiter(rate_limits_backend, "distributed-mutex-report", limit=1)


@dramatiq.actor(max_retries=0, store_results=True)
def dispatch_taking_screenshots():
    """Checks games on a specified in settings server and dispatches group of tasks
    for taking screenshots

    :return: a dictionary in which keys are game identifiers and values are lists
    of screenshot files
    :rtype: dict
    """
    logger.debug('Dispatching taking games screenshots tasks')
    try:
        group = dramatiq.group(take_sized_screenshots_by_game_id.message(game_id)
                               for game_id in funcs.get_games_ids())
        group.run()
        # Dictionary to collect game identifiers as keys and screenshot file name
        # lists as values for report
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
def take_sized_screenshots_by_game_id(game_id):
    """Takes screenshots with regards to required sizes which are specified in
    settings

    :param game_id: a game identifier
    :type game_id: int
    :return: a tuple with a game identifier and a list of screenshot files
    :rtype: (int, list)
    """
    logger.debug('Taking screenshots: %s', game_id)
    try:
        files = funcs.take_sized_screenshots_by_game_id(game_id)
        return game_id, files
    except ParseError as e:
        logger.error('Parse error: %s', e)
    except APIError as e:
        logger.error('API response error: %s', e)
    return game_id, None


@dramatiq.actor(max_retries=5)
def write_games_screenshots_json_report(games_screenshots):
    """Writes a JSON report with given data. The output file name is specified
    in settings

    :param games_screenshots: a data to be written as a report
    :type games_screenshots: dict
    """
    if games_screenshots:
        logger.debug('Report games: %s', games_screenshots)
    with DISTRIBUTED_MUTEX_REPORT.acquire():
        funcs.write_games_screenshots_json_report(games_screenshots)


@dramatiq.actor(max_retries=1)
def delete_expired_screenshots_cache():
    """Deletes expired screenshot cache
    """
    with DISTRIBUTED_MUTEX_REPORT.acquire():
        exclude_screenshots = funcs.get_latest_screenshots_file_names()

    funcs.delete_screenshots(exclude_screenshots)
