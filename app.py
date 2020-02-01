import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from lib import settings
from lib.actors import dispatch_taking_screenshots


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        dispatch_taking_screenshots.send,
        IntervalTrigger(seconds=settings.TASK_INTERVAL),
    )
    try:
        logger.info("Start scheduler")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Shutdown scheduler")
        scheduler.shutdown()


if __name__ == '__main__':
    main()
