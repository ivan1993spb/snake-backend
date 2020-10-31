
from typing import List

from pydantic import BaseModel


class Game(BaseModel):
    id: int
    limit: int
    count: int
    width: int
    height: int
    rate: int


class Games(BaseModel):
    games: List[Game]
    limit: int
    count: int


class DeletedGame(BaseModel):
    id: int


class Broadcast(BaseModel):
    success: bool


class Pong(BaseModel):
    pong: int


class Info(BaseModel):
    author: str
    license: str
    version: str
    build: str


class Capacity(BaseModel):
    capacity: float


class Map(BaseModel):
    width: int
    height: int


class Objects(BaseModel):
    objects: List[dict]
    map: Map
