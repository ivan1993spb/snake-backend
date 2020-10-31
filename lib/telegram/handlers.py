
from abc import ABC, abstractmethod
from typing import Tuple

from telegram import Bot

from lib.telegram.state import State


class BaseUpdateHandler(ABC):
    """Base class for all telegram update handlers
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        raise NotImplementedError


class UpdateHandlerDefault(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerShowGame(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerDeleteGameConfirmation(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitSize(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitPlayersLimit(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []


class UpdateHandlerCreateGameSubmitWalls(BaseUpdateHandler):

    def handle(self,
               chat_id: int,
               args: tuple,
               state_data: list) -> Tuple[State, list]:
        return State.DEFAULT, []
