"""The module contains states for the telegram bot
"""
from enum import Enum


class Command(int, Enum):
    START = 1
    RULES = 2
    LIST_GAMES = 3
    SHOW_GAME = 4
    SHOW_HELP = 5
    SHOW_INFO = 6
