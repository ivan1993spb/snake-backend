import logging

import dramatiq

import lib.funcs
from lib import settings


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


@dramatiq.actor(max_retries=0)
def dispatch_taking_screenshots():
    logger.info('Dispatching taking games screenshots tasks')
    for game_id in lib.funcs.get_games_ids():
        take_sized_screenshots_by_game_id.send(game_id)


@dramatiq.actor(max_retries=0)
def take_sized_screenshots_by_game_id(game_id):
    logger.info('Taking screenshots: %s', game_id)
    lib.funcs.take_sized_screenshots_by_game_id(game_id)
