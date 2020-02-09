"""The module contains classes to parse server responses
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

from lib.objects import (
    OBJECT_TYPE_APPLE,
    OBJECT_TYPE_CORPSE,
    OBJECT_TYPE_SNAKE,
    OBJECT_TYPE_WALL,
    OBJECT_TYPE_WATERMELON,
    OBJECT_TYPE_MOUSE,
    OBJECT_TYPE_UNKNOWN,
)


class ParseError(Exception):
    pass


class ParseObjectError(ParseError):
    pass


class ObjectParser:
    """Parses a raw object and returns an instance of a suitable class
    """

    FIELD_LABEL_TYPE = 'type'
    FIELD_LABEL_DOT = 'dot'
    FIELD_LABEL_DOTS = 'dots'

    OBJECT_LABEL_APPLE = 'apple'
    OBJECT_LABEL_CORPSE = 'corpse'
    OBJECT_LABEL_SNAKE = 'snake'
    OBJECT_LABEL_WALL = 'wall'
    OBJECT_LABEL_WATERMELON = 'watermelon'
    OBJECT_LABEL_MOUSE = 'mouse'

    __cast_object_labels_object_types = {
        OBJECT_LABEL_APPLE: OBJECT_TYPE_APPLE,
        OBJECT_LABEL_CORPSE: OBJECT_TYPE_CORPSE,
        OBJECT_LABEL_SNAKE: OBJECT_TYPE_SNAKE,
        OBJECT_LABEL_WALL: OBJECT_TYPE_WALL,
        OBJECT_LABEL_WATERMELON: OBJECT_TYPE_WATERMELON,
        OBJECT_LABEL_MOUSE: OBJECT_TYPE_MOUSE,
    }

    @staticmethod
    def parse(raw_object: dict):
        """Parses raw object dictionary and returns object type and dots

        :param raw_object: raw object entity
        :return: object type identifier and dots
        :rtype: (int, list)
        """
        try:
            object_type_label = raw_object[ObjectParser.FIELD_LABEL_TYPE]
            object_type = ObjectParser.__cast_object_labels_object_types.get(object_type_label, OBJECT_TYPE_UNKNOWN)

            if ObjectParser.FIELD_LABEL_DOT in raw_object:
                return object_type, [raw_object[ObjectParser.FIELD_LABEL_DOT]]
            if ObjectParser.FIELD_LABEL_DOTS in raw_object:
                return object_type, raw_object[ObjectParser.FIELD_LABEL_DOTS]

        except KeyError as e:
            raise ParseObjectError() from e

        return OBJECT_TYPE_UNKNOWN, []


class ParseMapSizeParserError(ParseError):
    pass


class MapSizeParser:
    """Parses map size entity
    """

    LABEL_WIDTH = 'width'
    LABEL_HEIGHT = 'height'

    @staticmethod
    def parse(raw_map_size: dict):
        """Parses raw map size entity and returns a tuple with width and height

        :param raw_map_size: raw map size entity
        :return: width and height of a map
        :rtype: (int, int)
        """
        try:
            return (
                raw_map_size[MapSizeParser.LABEL_WIDTH],
                raw_map_size[MapSizeParser.LABEL_HEIGHT],
            )
        except KeyError as e:
            raise ParseMapSizeParserError() from e


class GamesParser:
    """Parses games entity
    """

    LABEL_GAMES = 'games'
    LABEL_GAME_ID = 'id'

    @staticmethod
    def parse(raw_games: dict):
        """Parses raw game entity and returns a generator with game identifiers

        :param raw_games: raw games entity
        :return: a generator with game identifiers
        """
        for game in raw_games[GamesParser.LABEL_GAMES]:
            yield game[GamesParser.LABEL_GAME_ID]


class ParseObjectsError(ParseError):
    pass


class ObjectsParser:
    """Splits a raw objects response for raw map entity and raw objects entity.
    """

    LABEL_OBJECTS = 'objects'
    LABEL_MAP = 'map'

    @staticmethod
    def parse(raw_objects: dict):
        """Parses a raw objects response and splits it in two entities with raw map info
        and raw objects info.

        :param raw_objects: a raw objects response
        :return: raw map entity and raw objects entity
        :rtype: (dict, dict)
        """
        try:
            return (
                raw_objects[ObjectsParser.LABEL_MAP],
                raw_objects[ObjectsParser.LABEL_OBJECTS],
            )
        except KeyError as e:
            raise ParseObjectsError() from e
