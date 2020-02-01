from lib.objects import (
    OBJECT_TYPE_APPLE,
    OBJECT_TYPE_CORPSE,
    OBJECT_TYPE_SNAKE,
    OBJECT_TYPE_WALL,
    OBJECT_TYPE_WATERMELON,
    OBJECT_TYPE_MOUSE,
    OBJECT_TYPE_UNKNOWN,
)


class ParseObjectError(Exception):
    pass


class ObjectParser:
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


class ParseMapSizeParserError(Exception):
    pass


class MapSizeParser:
    LABEL_WIDTH = 'width'
    LABEL_HEIGHT = 'height'

    @staticmethod
    def parse(raw_map_size: dict):
        try:
            return (
                raw_map_size[MapSizeParser.LABEL_WIDTH],
                raw_map_size[MapSizeParser.LABEL_HEIGHT],
            )
        except KeyError as e:
            raise ParseMapSizeParserError() from e


class GamesParser:
    LABEL_GAMES = 'games'
    LABEL_GAME_ID = 'id'

    @staticmethod
    def parse(raw_games: dict):
        for game in raw_games[GamesParser.LABEL_GAMES]:
            yield game[GamesParser.LABEL_GAME_ID]


class ObjectsParser:
    LABEL_OBJECTS = 'objects'
    LABEL_MAP = 'map'

    @staticmethod
    def parse(raw_objects: dict):
        return raw_objects[ObjectsParser.LABEL_MAP], raw_objects[ObjectsParser.LABEL_OBJECTS]
