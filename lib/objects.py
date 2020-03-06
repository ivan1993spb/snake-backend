"""The module specifies objects which could be placed on a map, class-factory
initializing objects.
"""

from typing import Tuple, Generator, List

from lib.color import COLOR_RGB


OBJECT_TYPE_APPLE = 1
OBJECT_TYPE_CORPSE = 2
OBJECT_TYPE_SNAKE = 3
OBJECT_TYPE_WALL = 4
OBJECT_TYPE_WATERMELON = 5
OBJECT_TYPE_MOUSE = 6
OBJECT_TYPE_UNKNOWN = 7


DOT = Tuple[int, int]
DOTS = List[DOT]


class Object:
    """Stub object
    """
    COLOR: COLOR_RGB = (0x0, 0x0, 0x0)

    def __init__(self, dots: DOTS):
        """Initializes an object with passed dots.

        Parameters:
          dots: dots of an object
        """
        self._dots = dots

    def dots(self) -> Generator[Tuple[DOT, COLOR_RGB], None, None]:
        """Returns a generator with dots

        Returns:
          A generator with tuples as items which contain dots and colors.
        """
        for dot in self._dots:
            x, y = dot
            yield (x, y), self.COLOR


class Apple(Object):
    COLOR: COLOR_RGB = (0x0, 0xff, 0x0)


class Corpse(Object):
    COLOR: COLOR_RGB = (0x0, 0x0, 0xff)


class Snake(Object):
    COLOR: COLOR_RGB = (0xff, 0x44, 0x44)


class Wall(Object):
    COLOR: COLOR_RGB = (0x44, 0x77, 0x44)


class Watermelon(Object):
    COLOR: COLOR_RGB = (0xf0, 0xff, 0x0)


class Mouse(Object):
    COLOR: COLOR_RGB = (0xff, 0x0, 0x0)


class Unknown(Object):
    COLOR: COLOR_RGB = (0x66, 0x66, 0x66)


class ObjectFactory:
    """Creates an object of a special type using object class
    """

    __cast_object_types_classes = {
        OBJECT_TYPE_APPLE: Apple,
        OBJECT_TYPE_CORPSE: Corpse,
        OBJECT_TYPE_SNAKE: Snake,
        OBJECT_TYPE_WALL: Wall,
        OBJECT_TYPE_WATERMELON: Watermelon,
        OBJECT_TYPE_MOUSE: Mouse,
        OBJECT_TYPE_UNKNOWN: Unknown,
    }

    @staticmethod
    def create(object_type: int, dots: DOTS):
        """Casts given object type with a class of the object and tries to
        create an object instance. If succeed, returns the object instance.

        Parameters:
          object_type: object type identifier
          dots: list of dots

        Returns:
          Am object of certain type.
        """
        return ObjectFactory.__cast_object_types_classes[object_type](dots)
