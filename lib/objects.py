OBJECT_TYPE_APPLE = 1
OBJECT_TYPE_CORPSE = 2
OBJECT_TYPE_SNAKE = 3
OBJECT_TYPE_WALL = 4
OBJECT_TYPE_WATERMELON = 5
OBJECT_TYPE_MOUSE = 6
OBJECT_TYPE_UNKNOWN = 7


class Object:
    COLOR = (0x0, 0x0, 0x0)

    def __init__(self, dots):
        self._dots = dots

    def dots(self):
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
        return ObjectFactory.__cast_object_types_classes[object_type](dots)
