
from enum import Enum
from typing import List, Tuple, Union
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


Dot = Tuple[int, int]

ColorRGB = Tuple[int, int, int]


COLOR_RGB_APPLE: ColorRGB = (0x0, 0xff, 0x0)
COLOR_RGB_CORPSE: ColorRGB = (0x0, 0x0, 0xff)
COLOR_RGB_MOUSE: ColorRGB = (0xff, 0x0, 0x0)
COLOR_RGB_SNAKE: ColorRGB = (0xff, 0x44, 0x44)
COLOR_RGB_WALL: ColorRGB = (0x44, 0x77, 0x44)
COLOR_RGB_WATERMELON: ColorRGB = (0xf0, 0xff, 0x0)


OBJECT_LABEL_APPLE = 'apple'
OBJECT_LABEL_CORPSE = 'corpse'
OBJECT_LABEL_MOUSE = 'mouse'
OBJECT_LABEL_SNAKE = 'snake'
OBJECT_LABEL_WALL = 'wall'
OBJECT_LABEL_WATERMELON = 'watermelon'


class Game(BaseModel):
    """Game schema
    """

    id: int
    limit: int
    count: int
    width: int
    height: int
    rate: int

    def is_full(self) -> bool:
        return self.count == self.limit

    def is_playable(self) -> bool:
        return 0 < self.count < self.limit

    def is_empty(self) -> bool:
        return self.count == 0


class OneDotObject(ABC):
    """Any game object which consists of one dot
    """

    dot: Dot

    @property
    def dots(self) -> List[Dot]:
        """List of dots
        """
        return [self.dot]


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
    """Schema of the server's capacity
    """

    capacity: float


class Map(BaseModel):
    """Schema of map proportions
    """

    width: int
    height: int


class ObjectType(str, Enum):
    """Game objects types enumeration
    """

    apple = OBJECT_LABEL_APPLE
    corpse = OBJECT_LABEL_CORPSE
    mouse = OBJECT_LABEL_MOUSE
    snake = OBJECT_LABEL_SNAKE
    wall = OBJECT_LABEL_WALL
    watermelon = OBJECT_LABEL_WATERMELON


class Colored(ABC):
    """Abstract class for all colored objects
    """

    @staticmethod
    @abstractmethod
    def color() -> ColorRGB: return 0, 0, 0


class Apple(BaseModel, Colored, OneDotObject):
    """Game object: an apple
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.apple)
    dot: Dot

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_APPLE


class Corpse(BaseModel, Colored):
    """Game object: a corpse
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.corpse)
    dots: List[Dot]

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_CORPSE


class Mouse(BaseModel, Colored, OneDotObject):
    """Game object: a mouse
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.mouse)
    dot: Dot
    direction: str

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_MOUSE


class Snake(BaseModel, Colored):
    """Game object: a snake
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.snake)
    dots: List[Dot]

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_SNAKE


class Wall(BaseModel, Colored):
    """Game object: a wall
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.wall)
    dots: List[Dot]

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_WALL


class Watermelon(BaseModel, Colored):
    """Game object: a watermelon
    """

    id: int
    type: ObjectType = Field(const=True, default=ObjectType.watermelon)
    dots: List[Dot]

    @staticmethod
    def color() -> ColorRGB: return COLOR_RGB_WATERMELON


AnyObject = Union[Apple, Corpse, Mouse, Snake, Wall, Watermelon]

AnyObjectList = List[AnyObject]


class Objects(BaseModel):
    """A schema of response of the server for game's object list
    """

    objects: AnyObjectList
    map: Map
