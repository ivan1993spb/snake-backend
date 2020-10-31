
from enum import Enum
from typing import List, Tuple, Union

from pydantic import BaseModel
from num2words import num2words


# TODO: Use color from pydantic?
# from pydantic.color import Color


Dot = Tuple[int, int]


class Game(BaseModel):
    id: int
    limit: int
    count: int
    width: int
    height: int
    rate: int

    @property
    def name(self) -> str:
        return num2words(self.id)

    def is_full(self) -> bool:
        return self.count == self.limit

    def is_playable(self) -> bool:
        return 0 < self.count < self.limit

    def is_empty(self) -> bool:
        return self.count == 0


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


class ObjectType(str, Enum):
    apple = 'apple'
    corpse = 'corpse'
    mouse = 'mouse'
    snake = 'snake'
    wall = 'wall'
    watermelon = 'watermelon'


class Apple(BaseModel):
    id: int
    type = ObjectType.apple
    dot: Dot

    @property
    def dots(self) -> List[Dot]: return [self.dot]


class Corpse(BaseModel):
    id: int
    type = ObjectType.corpse
    dots: List[Dot]


class Mouse(BaseModel):
    id: int
    type = ObjectType.mouse
    dot: Dot
    direction: str

    @property
    def dots(self) -> List[Dot]: return [self.dot]


class Snake(BaseModel):
    id: int
    type = ObjectType.snake
    dots: List[Dot]


class Wall(BaseModel):
    id: int
    type = ObjectType.wall
    dots: List[Dot]


class Watermelon(BaseModel):
    id: int
    type = ObjectType.watermelon
    dots: List[Dot]


AnyObject = Union[Apple, Corpse, Mouse, Snake, Wall, Watermelon]

# TODO: Define the proper type
# AnyObjectList = List[AnyObject]
AnyObjectList = List[dict]


class Objects(BaseModel):
    objects: AnyObjectList
    map: Map
