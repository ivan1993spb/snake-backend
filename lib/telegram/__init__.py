
from typing import Dict, Tuple
import pickle

import telegram
import redis

from lib.telegram.state import State
from lib.telegram.handlers import (
    BaseUpdateHandler,
    UpdateHandlerDefault,
    UpdateHandlerShowGame,
    UpdateHandlerDeleteGameConfirmation,
    UpdateHandlerCreateGameSubmitSize,
    UpdateHandlerCreateGameSubmitPlayersLimit,
    UpdateHandlerCreateGameSubmitWalls,
)
from lib.telegram.command import Command


class TelegramBotException(Exception):
    pass


class TelegramBot:
    """Telegram updates handler
    """

    # Hold chat states and variables for 1h
    EXPIRE_SECONDS = 3600

    _bot: telegram.Bot
    _redis_client: redis.Redis
    _handlers: Dict[State, BaseUpdateHandler]

    def __init__(self, bot: telegram.Bot, redis_client: redis.Redis):
        self._bot = bot
        self._redis_client = redis_client
        self._handlers = {
            State.DEFAULT:
                UpdateHandlerDefault(bot),
            State.SHOW_GAME:
                UpdateHandlerShowGame(bot),
            State.DELETE_GAME_CONFIRMATION:
                UpdateHandlerDeleteGameConfirmation(bot),
            State.CREATE_GAME_SUBMIT_SIZE:
                UpdateHandlerCreateGameSubmitSize(bot),
            State.CREATE_GAME_SUBMIT_PLAYERS_LIMIT:
                UpdateHandlerCreateGameSubmitPlayersLimit(bot),
            State.CREATE_GAME_SUBMIT_WALLS:
                UpdateHandlerCreateGameSubmitWalls(bot),
        }

    def _get_chat_state_data(self, chat_id: int) -> Tuple[State, list]:
        chat_stored_data = self._redis_client.get(chat_id)

        if chat_stored_data is None:
            return State.DEFAULT, []

        chat_data: list

        try:
            chat_data = list(pickle.loads(chat_stored_data))
        except pickle.UnpicklingError:
            # Clear whatever is stored for the given chat id
            self._redis_client.delete(chat_id)
            return State.DEFAULT, []

        if not chat_data:
            return State.DEFAULT, []

        chat_state, *state_data = chat_data

        return chat_state, state_data

    def _set_chat_state_data(self,
                             chat_id: int,
                             chat_state: State,
                             state_data: list):

        chat_data = [chat_state, *state_data]

        try:
            encoded_chat_data = pickle.dumps(chat_data)
            self._redis_client.setex(chat_id,
                                     self.EXPIRE_SECONDS,
                                     encoded_chat_data)
        except pickle.PicklingError as e:
            raise TelegramBotException('Cannot save chat data') from e

    def _get_handler(self, chat_state: State) -> BaseUpdateHandler:
        return self._handlers.get(chat_state, self._handlers[State.DEFAULT])

    def handle(self, chat_id: int, cmd: Command, args: tuple):
        chat_state, state_data = self._get_chat_state_data(chat_id)
        handler = self._get_handler(chat_state)
        next_chat_state, next_state_data = handler.handle(chat_id,
                                                          cmd,
                                                          args,
                                                          state_data)
        self._set_chat_state_data(chat_id, next_chat_state, next_state_data)
