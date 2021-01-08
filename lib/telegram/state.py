"""The module contains states for the telegram bot
"""
from enum import Enum
from typing import Dict, List

from lib.telegram.command import Command


class State(int, Enum):
    # TODO: Delete ANY state.
    ANY = 0
    DEFAULT = 1
    SHOW_GAME = 2
    DELETE_GAME_CONFIRMATION = 3
    CREATE_GAME_SUBMIT_SIZE = 4
    CREATE_GAME_SUBMIT_PLAYERS_LIMIT = 5
    CREATE_GAME_SUBMIT_WALLS = 6


STATES_COMMANDS: Dict[State, List[Command]] = {
    State.DEFAULT: [
        Command.START,
        Command.RULES,
        Command.LIST_GAMES,
    ],
}
