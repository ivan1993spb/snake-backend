
from abc import ABC, abstractmethod
from typing import Tuple, Dict

from telegram import Bot
from telegram.parsemode import ParseMode

from lib.telegram.command import Command
from lib.telegram.state import State
from lib.telegram import messages


class BaseUpdateProcessor(ABC):
    """Base class for all telegram update handlers
    """

    def __init__(self, bot: Bot):
        self._bot = bot

    @abstractmethod
    def process(self,
                chat_id: int,
                cmd: Command,
                args: tuple,
                state: State,
                state_data: list) -> Tuple[State, list]:
        """The method process a command in a given context which includes
        a state, stored data, and a set of arguments.

        Parameters:
          chat_id: a telegram chat identifier.
          cmd: telegram command.
          args: command arguments.
          state: current chat state.
          state_data: stored data.
        """
        raise NotImplementedError


class HelpCommandProcessor(BaseUpdateProcessor):
    HELP_MESSAGES: Dict[State, str] = {
        State.DEFAULT: messages.HELP_DEFAULT,
        State.SHOW_GAME: messages.HELP_SHOW_GAME,
        # TODO: Add more states and messages.
        # State.DELETE_GAME_CONFIRMATION = 3
        # State.CREATE_GAME_SUBMIT_SIZE = 4
        # State.CREATE_GAME_SUBMIT_PLAYERS_LIMIT = 5
        # State.CREATE_GAME_SUBMIT_WALLS = 6
    }

    def process(self, chat_id: int, cmd: Command, args: tuple, state: State,
                state_data: list) -> Tuple[State, list]:

        help_message = self.HELP_MESSAGES.get(state, messages.NO_HELP)

        self._bot.send_message(chat_id=chat_id,
                               text=help_message,
                               parse_mode=ParseMode.MARKDOWN_V2)

        return state, state_data
