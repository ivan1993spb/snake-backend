"""The module contains a number of actors to be executed by a schedule. The
actors provide some necessary operations with the Snake-Server such as
screenshot generation and so on.
"""

import logging
from typing import Tuple, Dict, List

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
from pydantic import ValidationError

from lib import settings
from lib import funcs
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
    except ValidationError as e:
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
    except ValidationError as e:
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
