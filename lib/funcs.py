"""The module contains a set of functions which provides the operations with
the Snake-Server instance
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import os
import os.path
import json
import itertools

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
    """
    :return: Client object to connect to the Snake-Server
    :rtype: APIClient
    """
    return APIClient(settings.SNAKE_API_ADDRESS, settings.CLIENT_NAME)


def get_games_ids():
    """Returns games identifiers

    :rtype: list
    """
    client = get_api_client()
    raw_games = client.get_games()
    return GamesParser.parse(raw_games)


def get_game_objects(game_id):
    """Returns map size and game objects

    :rtype: ((int, int), list)
    :raises: APIError, ParseError
    """
    client = get_api_client()
    raw_data = client.get_game_objects(game_id)

    raw_map_size, raw_objects = ObjectsParser.parse(raw_data)
    map_size = MapSizeParser.parse(raw_map_size)
    objects = []
    for raw_object in raw_objects:
        object_type, dots = ObjectParser.parse(raw_object)
        objects.append(ObjectFactory.create(object_type, dots))
    return map_size, objects


def generate_screenshot_image(map_size: tuple, max_size: tuple, objects: list, strict_sized: bool):
    """Generates screenshot image.

    :param map_size: size of map in dots
    :type map_size: (int, int)
    :param max_size: limits for result image in px
    :type max_size: (int, int)
    :param objects: list of game objects
    :param strict_sized: a flag whether to generate an image with strict limited size or not
    :return: image instance
    """
    screenshot = Screenshot(map_size, max_size, objects, strict_sized)
    return screenshot.img


def get_image_path(game_id, map_size: tuple, size_slug):
    """Returns an image destination path

    :param game_id:
    :param map_size:
    :param size_slug:
    :return: path string
    """
    width, height = map_size
    return os.path.join(settings.SCREENSHOT_DEST_PATH,
                        'g{}s{}x{}-{}.jpeg'.format(game_id, width, height, size_slug))


def save_objects_as_screenshot(path: str,
                               map_size: tuple,
                               max_size: tuple,
                               objects: list,
                               quality: int,
                               strict_sized: bool):
    """Saves given objects as a screenshot file.

    :param path: path destination
    :param map_size: size of map in dots
    :type map_size: (int, int)
    :param max_size: limits for result image in px
    :type max_size: (int, int)
    :param objects: list of game objects
    :param quality: quality
    :param strict_sized: a flag whether to generate an image with strict limited size or not
    """
    img = generate_screenshot_image(map_size, max_size, objects, strict_sized)
    img.save(path, quality=quality, optimize=True)


def take_sized_screenshots_by_game_id(game_id):
    """Takes a screenshot for a game with given game identifier and returns list of file names.

    :param game_id: game identifier
    :return: list of file names
    :rtype: list
    """
    map_size, objects = get_game_objects(game_id)
    files = []
    for size_slug, length in settings.SCREENSHOT_LENGTHS.items():
        path = get_image_path(game_id, map_size, size_slug)
        save_objects_as_screenshot(path,
                                   map_size,
                                   (length, length),
                                   objects,
                                   settings.SCREENSHOT_QUALITY,
                                   settings.SCREENSHOT_STRICT_SIZED)
        files.append(os.path.basename(path))
    return files


def get_json_report_path():
    """Returns a path to a screenshot report location.

    :return: path
    :rtype: str
    """
    return os.path.join(settings.SCREENSHOT_DEST_PATH, settings.SCREENSHOTS_JSON_FILE)


def write_games_screenshots_json_report(games_screenshots):
    """Writes a JSON report.

    :param games_screenshots: a report object to be JSON encoded and written in file.
    """
    if games_screenshots:
        with open(get_json_report_path(), 'w') as fp:
            json.dump(games_screenshots, fp)


def read_games_screenshots_json_report() -> dict:
    """Reads and returns JSON screenshots report.
    """
    try:
        with open(get_json_report_path(), 'r') as fp:
            return json.load(fp)
    except IOError:
        return {}


def get_latest_screenshots_file_names() -> tuple:
    """Returns a tuple of latest screenshots file names.
    """
    return tuple(itertools.chain.from_iterable(
        read_games_screenshots_json_report().values()))


def delete_screenshots(exclude_screenshots: tuple):
    """Deletes expired screenshot cache

    :param exclude_screenshots: screenshots which are not to be deleted
    """
    for filename in os.listdir(settings.SCREENSHOT_DEST_PATH):
        if filename.endswith('.jpeg') and filename not in exclude_screenshots:
            file_path = os.path.join(settings.SCREENSHOT_DEST_PATH, filename)
            os.remove(file_path)
