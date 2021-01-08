
from abc import ABC, abstractmethod
from typing import Tuple
from pathlib import Path

from telegram import Bot
from telegram.parsemode import ParseMode

from lib.telegram.state import State
from lib.telegram.command import Command
from lib.telegram import messages
from lib import funcs
from lib import settings


class BaseUpdateHandler(ABC):
    """Base class for all telegram update handlers
    """

    def __init__(self, bot: Bot):
        self._bot = bot

    @abstractmethod
    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        raise NotImplementedError


class UpdateHandlerDefault(BaseUpdateHandler):

    def __init__(self, bot: Bot):
        self._commands = {
            Command.START: self._cmd_start,
            Command.RULES: self._cmd_rules,
            Command.LIST_GAMES: self._cmd_list_games,
        }
        super().__init__(bot)

    def _cmd_start(self, chat_id,
                   args: tuple,
                   state_data: list) -> Tuple[State, list]:
        self._bot.send_message(chat_id,
                               text=messages.WELCOME_MESSAGE,
                               parse_mode=ParseMode.MARKDOWN_V2)
        return State.DEFAULT, []

    def _cmd_rules(self, chat_id,
                   args: tuple,
                   state_data: list) -> Tuple[State, list]:
        self._bot.send_message(chat_id,
                               text=messages.RULES,
                               parse_mode=ParseMode.MARKDOWN_V2)
        return State.DEFAULT, []

    def _cmd_list_games(self, chat_id,
                        args: tuple,
                        state_data: list) -> Tuple[State, list]:
        games = funcs.sort_games(funcs.get_games())

        # TODO: Add constant
        if len(games) > 10:
            games = games[:10]

        game_lines = []
        for game in games:
            game_lines.append(f'\\* _game {funcs.get_game_name(game)}_ '
                              f'`{game.count}/{game.limit}` '
                              f'/show\\_{game.id}')

        # TODO: Add emoji.
        text = f'*Games*\n\n' + '\n'.join(game_lines)

        self._bot.send_message(chat_id=chat_id,
                               text=text,
                               parse_mode=ParseMode.MARKDOWN_V2)

        return State.DEFAULT, []

    def _cmd_show_game(self, chat_id,
                       args: tuple,
                       state_data: list) -> Tuple[State, list]:
        game_id = args[0]
        game = funcs.get_game(game_id)

        # TODO: Move the code to the funcs module.
        # TODO: Delete only if 0 gamers
        # TODO: Add emoji.
        text = f'*Game {funcs.get_game_name(game)}*\n\n' \
               f'_Players_: `{game.count}/{game.limit}`\n' \
               f'_Size_: `{game.width}x{game.height}`\n' \
               f'_Rate_: `{game.rate}pps`\n\n' \
               f'/delete\\_{game.id}\n\n' \
               f'[Play now\\!]({funcs.get_game_link(game)})\n\n' \
               f'Back /list'

        image_path = funcs.get_image_path(game_id,
                                          (game.width, game.height),
                                          settings.SCREENSHOT_SLUG_MEDIUM)
        if Path(image_path).is_file():
            self._bot.send_photo(
                chat_id=chat_id,
                photo=open(image_path, 'rb'),
                caption=text,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
            self._bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview='True',
            )

        return State.SHOW_GAME, [game_id]

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        print(chat_id, args, state_data)

        # TODO: Add checks.
        self._commands.get(cmd)(chat_id, args, state_data)

        return State.DEFAULT, []


class UpdateHandlerShowGame(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerDeleteGameConfirmation(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitSize(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitPlayersLimit(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitWalls(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               cmd: Command,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []
