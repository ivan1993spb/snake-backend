"""The module contains a set of functions which provides the operations with
the Snake-Server instance
"""

import os
import os.path
import json
import itertools
from typing import List, Tuple, Dict

from PIL import Image

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


def get_api_client() -> APIClient:
    """Returns a client object to connect to the Snake-Server.
    """
    return APIClient(settings.SNAKE_API_ADDRESS, settings.CLIENT_NAME)


def get_games_ids() -> List[int]:
    """Returns games identifiers.
    """
    client = get_api_client()
    raw_games = client.get_games()
    return list(GamesParser.parse(raw_games))


def get_game_objects(game_id: int) -> Tuple[Tuple[int, int], list]:
    """Returns map size and game objects.

    Parameters:
      game_id: a game identifier.

    Raises:
      APIError: when Rest API has returned an error.
      ParseError: when there has been incorrect response.
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


def generate_screenshot_image(map_size: Tuple[int, int],
                              max_size: Tuple[int, int],
                              objects: list,
                              strict_sized: bool) -> Image:
    """Generates screenshot image.

    Parameters:
      map_size: size of map in dots
      max_size: limits for result image in px
      objects: list of game objects
      strict_sized: a flag whether to generate an image with strict limited size or not

    Returns:
      An image instance.
    """
    screenshot = Screenshot(map_size, max_size, objects, strict_sized)
    return screenshot.img


def get_image_path(game_id: int,
                   map_size: Tuple[int, int],
                   size_slug: str) -> str:
    """Returns an image destination path

    Parameters:
      game_id: a game identifier
      map_size: map size width and height
      size_slug: slug for a file name

    Returns:
      A path string
    """
    width, height = map_size
    return os.path.join(settings.SCREENSHOT_DEST_PATH,
                        'g{}s{}x{}-{}.jpeg'.format(game_id,
                                                   width,
                                                   height,
                                                   size_slug))


def save_objects_as_screenshot(path: str,
                               map_size: Tuple[int, int],
                               max_size: Tuple[int, int],
                               objects: list,
                               quality: int,
                               strict_sized: bool):
    """Saves given objects as a screenshot file.

    Parameters:
      path: path destination
      map_size: size of map in dots
      max_size: limits for result image in px
      objects: list of game objects
      quality: quality
      strict_sized: a flag whether to generate an image with strict limited size or not
    """
    img = generate_screenshot_image(map_size, max_size, objects, strict_sized)
    img.save(path, quality=quality, optimize=True)


def take_sized_screenshots_by_game_id(game_id: int) -> List[str]:
    """Takes a screenshot for a game with given game identifier and returns list of file names.

    Parameters:
      game_id: a game identifier.

    Returns:
      A list of file names.
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


def get_json_report_path() -> str:
    """Returns a path to a screenshot report location.
    """
    return os.path.join(settings.SCREENSHOT_DEST_PATH,
                        settings.SCREENSHOTS_JSON_FILE)


def write_games_screenshots_json_report(
        games_screenshots: Dict[int, List[str]]):
    """Writes a JSON report.

    Parameters:
      games_screenshots: a report object to be JSON encoded and written in file.
    """
    if games_screenshots:
        with open(get_json_report_path(), 'w') as fp:
            json.dump(games_screenshots, fp)


def read_games_screenshots_json_report() -> Dict[int, List[str]]:
    """Reads and returns JSON screenshots report.
    """
    try:
        with open(get_json_report_path(), 'r') as fp:
            return json.load(fp)
    except IOError:
        return {}


def get_latest_screenshots_file_names() -> Tuple[str]:
    """Returns a tuple of latest screenshots file names.
    """
    return tuple(itertools.chain.from_iterable(
        read_games_screenshots_json_report().values()))


def delete_screenshots(exclude_screenshots: Tuple[str]):
    """Deletes expired screenshot cache

    Parameters:
      exclude_screenshots: screenshots which are not to be deleted.
    """
    for filename in os.listdir(settings.SCREENSHOT_DEST_PATH):
        if filename.endswith('.jpeg') and filename not in exclude_screenshots:
            file_path = os.path.join(settings.SCREENSHOT_DEST_PATH, filename)
            os.remove(file_path)
