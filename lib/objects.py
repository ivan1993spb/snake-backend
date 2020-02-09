"""The module specifies objects which could be placed on a map, class-factory
initializing objects
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

OBJECT_TYPE_APPLE = 1
OBJECT_TYPE_CORPSE = 2
OBJECT_TYPE_SNAKE = 3
OBJECT_TYPE_WALL = 4
OBJECT_TYPE_WATERMELON = 5
OBJECT_TYPE_MOUSE = 6
OBJECT_TYPE_UNKNOWN = 7


class Object:
    """Stub object"""
    COLOR = (0x0, 0x0, 0x0)

    def __init__(self, dots):
        """Initializes an object with passed dots

        :param dots: dots of an object
        :type dots: list
        """
        self._dots = dots

    def dots(self):
        """Returns a generator with dots

        :return: generator with tuples as items which contain dots and colors
        """
        for dot in self._dots:
            x, y = dot
            yield (x, y), self.COLOR


class Apple(Object):
    COLOR = (0x0, 0xff, 0x0)


class Corpse(Object):
    COLOR = (0x0, 0x0, 0xff)


class Snake(Object):
    COLOR = (0xff, 0x44, 0x44)


class Wall(Object):
    COLOR = (0x44, 0x77, 0x44)


class Watermelon(Object):
    COLOR = (0xf0, 0xff, 0x0)


class Mouse(Object):
    COLOR = (0xff, 0x0, 0x0)


class Unknown(Object):
    COLOR = (0x66, 0x66, 0x66)


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
    def create(object_type, dots):
        """Casts given object type with a class of the object and tries to create an
        object instance. If succeed, returns the object instance.

        :param object_type: object type identifier
        :param dots: list of dots
        :type dots: list
        :return: object of certain type
        """
        return ObjectFactory.__cast_object_types_classes[object_type](dots)
