"""The application's entrypoint
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import logging
import pathlib

from dramatiq import pipeline
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from lib import settings
from lib.actors import (
    dispatch_taking_screenshots,
    write_games_screenshots_json_report,
    delete_expired_screenshots_cache,
)


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


def init():
    pathlib.Path(settings.SCREENSHOT_DEST_PATH).mkdir(parents=True, exist_ok=True)


def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        pipeline([
            dispatch_taking_screenshots.message(),
            write_games_screenshots_json_report.message(),
        ]).run,
        IntervalTrigger(seconds=settings.TASK_INTERVAL_SCREENSHOT),
        name="dispatch_taking_screenshots",
    )
    scheduler.add_job(
        delete_expired_screenshots_cache.send,
        IntervalTrigger(seconds=settings.TASK_INTERVAL_DELETE_CACHE),
        name="delete_expired_screenshots_cache",
    )
    try:
        logger.info("Start scheduler")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Shutdown scheduler")
        scheduler.shutdown()


def main():
    init()
    run_scheduler()


if __name__ == '__main__':
    main()
