
from typing import Dict, List

from lib.telegram.command import Command
from lib.telegram.state import State


MAPPING: Dict[Command, List[State]] = {
    Command.START: [State.DEFAULT],
    Command.RULES: [State.ANY],
    Command.SHOW_HELP: [State.ANY],
    Command.LIST_GAMES: [State.ANY],
    Command.SHOW_GAME: [State.ANY],
    Command.SHOW_INFO: [State.ANY],
    Command.CREATE_GAME: [State.DEFAULT],
    Command.DELETE_GAME: [State.SHOW_GAME],
    Command.RANDOM_GAME: [State.DEFAULT],

}
