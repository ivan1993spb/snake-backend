import os.path

from lib.api import APIClient
from lib import settings
from lib.parse import (
    MapSizeParser,
    GamesParser,
    ObjectsParser,
    ObjectParser,
)
from lib.objects import ObjectFactory
from lib.screenshot import Screenshot


def get_api_client():
    return APIClient(settings.SNAKE_API_ADDRESS, settings.CLIENT_NAME)


def get_games_ids():
    client = get_api_client()
    raw_games, ok = client.get_games()
    assert ok, raw_games
    return GamesParser.parse(raw_games)


def get_game_objects(game_id):
    client = get_api_client()
    raw_data, ok = client.get_game_objects(game_id)
    assert ok, raw_data

    raw_map_size, raw_objects = ObjectsParser.parse(raw_data)
    map_size = MapSizeParser.parse(raw_map_size)
    objects = []
    for raw_object in raw_objects:
        object_type, dots = ObjectParser.parse(raw_object)
        objects.append(ObjectFactory.create(object_type, dots))
    return map_size, objects


def generate_screenshot_image(map_size: tuple, max_size: tuple, objects: list, strict_sized: bool):
    screenshot = Screenshot(map_size, max_size, objects, strict_sized)
    return screenshot.img


def get_image_path(game_id, map_size: tuple, size_slug):
    width, height = map_size
    return os.path.join(settings.SCREENSHOT_DEST_PATH,
                        'g{}s{}x{}-{}.jpeg'.format(game_id, width, height, size_slug))


def save_as_screenshot(path: str,
                       map_size: tuple,
                       max_size: tuple,
                       objects: list,
                       quality: int,
                       strict_sized: bool):
    img = generate_screenshot_image(map_size, max_size, objects, strict_sized)
    img.save(path, quality=quality, optimize=True)


def take_sized_screenshots_by_game_id(game_id):
    map_size, objects = get_game_objects(game_id)
    for size_slug, length in settings.SCREENSHOT_LENGTHS.items():
        path = get_image_path(game_id, map_size, size_slug)
        save_as_screenshot(path,
                           map_size,
                           (length, length),
                           objects,
                           settings.SCREENSHOT_QUALITY,
                           settings.SCREENSHOT_STRICT_SIZED)
