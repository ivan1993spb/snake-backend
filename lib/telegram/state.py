"""The module contains states for the telegram bot
"""
from enum import Enum


class State(int, Enum):
    DEFAULT = 1
    SHOW_GAME = 2
    DELETE_GAME_CONFIRMATION = 3
    CREATE_GAME_SUBMIT_SIZE = 4
    CREATE_GAME_SUBMIT_PLAYERS_LIMIT = 5
    CREATE_GAME_SUBMIT_WALLS = 6
