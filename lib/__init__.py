import logging

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker

from lib import settings


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


if settings.UNIT_TESTS:
    dramatiq.set_broker(StubBroker())
else:
    logger.info("Setup redis broker")
    dramatiq.set_broker(RedisBroker(url=settings.REDIS_URL))
