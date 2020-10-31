
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


# redis_client = redis.Redis.from_url(url='')

class Bot:
    """Telegram updates handler
    """
    EXPIRE_SECONDS = 3600

    bot: telegram.Bot
    redis_client: redis.Redis
    handlers: Dict[State, BaseUpdateHandler]

    def __init__(self, bot: telegram.Bot, redis_client: redis.Redis):
        self.bot = bot
        self.redis_client = redis_client
        self.handlers = {
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
        chat_stored_data = self.redis_client.get(chat_id)

        if chat_stored_data is None:
            return State.DEFAULT, []

        chat_data: list

        try:
            chat_data = list(pickle.loads(chat_stored_data))
        except pickle.UnpicklingError:
            # Clear whatever is stored for the given chat id
            self.redis_client.delete(chat_id)
            return State.DEFAULT, []

        if not chat_data:
            return State.DEFAULT, []

        chat_state, *state_data = chat_data

        if chat_state not in self.handlers:
            # Delete data because the state is invalid
            self.redis_client.delete(chat_id)
            return State.DEFAULT, []

        return chat_state, state_data

    def _set_chat_state_data(self,
                             chat_id: int,
                             chat_state: State,
                             state_data: list):

        chat_data = [chat_state, *state_data]

        try:
            encoded_chat_data = pickle.dumps(chat_data)
            self.redis_client.setex(chat_id,
                                    self.EXPIRE_SECONDS,
                                    encoded_chat_data)

        except pickle.PicklingError:
            # TODO: raise an exception!
            pass

    def handle(self, chat_id: int, args: tuple):
        chat_state, state_data = self._get_chat_state_data(chat_id)
        handler = self.handlers[chat_state]
        next_chat_state, next_state_data = handler.handle(chat_id,
                                                          args,
                                                          state_data)
        self._set_chat_state_data(chat_id, next_chat_state, next_state_data)
