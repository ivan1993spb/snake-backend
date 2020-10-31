"""The module contains classes and methods to work with the API of
the Snake-Server.
"""

from typing import Tuple

from requests.utils import CaseInsensitiveDict
from requests import Session

from lib.schemas import (
    Broadcast,
    Capacity,
    DeletedGame,
    Game,
    Games,
    Info,
    Objects,
    Pong,
)


_PARAM_LABEL_LIMIT = 'limit'
_PARAM_LABEL_SORTING = 'sorting'

SORTING_SMART = 'smart'
SORTING_RANDOM = 'random'

_SORTING = (SORTING_SMART, SORTING_RANDOM)


class APIError(Exception):
    """Wraps an error which occurs in a process of request processing on
    server.
    """

    def __init__(self, status: int, text: str):
        """
        Parameters:
          status(int): a response status code
          text(str): a description of an error
        """
        self.status = status
        self.text = text

    def __str__(self):
        return 'status {}: {}'.format(self.status, self.text)


class APIClient(Session):
    _DEFAULT_USER_AGENT = 'SnakeAPIClient'

    # Field to look into in case of error
    _FIELD_TEXT = 'text'

    _DEFAULT_ERROR_MSG = 'undefined error'
    _RESPONSE_NOT_JSON_MSG = 'response supposed to be a valid json object'

    def __init__(self, api_address: str, user_agent: str = None):
        """
        Parameters:
          api_address(str): an API address
          user_agent(str): a user agent description to be sent to a server
        """
        assert api_address.endswith('/api'), 'API address must end with "/api"'

        super().__init__()

        self._api_address = api_address
        self._user_agent = user_agent or self._DEFAULT_USER_AGENT

        self.headers.update(self._initial_headers())

    def _initial_headers(self) -> CaseInsensitiveDict:
        """
        Returns:
          A dictionary with additional headers.
        """
        return CaseInsensitiveDict({
            'User-Agent': self._user_agent,
            'X-Snake-Client': self._user_agent,
            'Accept': 'application/json',
        })

    def get_games(self, limit: int = None, sorting: str = None) -> Games:
        """Returns information about ongoing games on a server.

        Returns:
          information about games.
        """
        params = {}
        if limit:
            params[_PARAM_LABEL_LIMIT] = limit
        if sorting:
            assert sorting in _SORTING, 'Invalid sorting type has been passed'
            params[_PARAM_LABEL_SORTING] = sorting
        raw = self._call('GET', 'games', params=params)
        return Games.parse_raw(raw)

    def get_game(self, game_id: int) -> Game:
        """Returns information about a game with specified game identifier.

        Parameters:
          game_id: a game identifier.
        """
        raw = self._call('GET', 'games', str(game_id))
        return Game.parse_raw(raw)

    def get_game_objects(self, game_id: int) -> Objects:
        """Returns information about game objects placed on a game map.

        Parameters:
          game_id: a game identifier.
        """
        raw = self._call('GET', 'games', str(game_id), 'objects')
        return Objects.parse_raw(raw)

    def delete_game(self, game_id: int) -> DeletedGame:
        """Sends a request for deleting a game.

        Parameters:
          game_id: a game identifier.
        """
        raw = self._call('DELETE', 'games', str(game_id))
        return DeletedGame.parse_raw(raw)

    def create_game(self, limit: int, width: int, height: int,
                    enable_walls: bool = True) -> Game:
        """Sends a request to create a game with given parameters.

        Parameters:
          limit: players limit.
          width: map width.
          height: map height.
          enable_walls: flag whether to add walls or not.
        """
        raw = self._call('POST', 'games', data={
            'limit': limit,
            'width': width,
            'height': height,
            'enable_walls': enable_walls,
        })
        return Game.parse_raw(raw)

    def broadcast(self, game_id: int, message: str) -> Broadcast:
        raw = self._call('POST', 'games', str(game_id), 'broadcast', data={
            'message': message,
        })
        return Broadcast.parse_raw(raw)

    def capacity(self) -> Capacity:
        """Sends a request to retrieve information about server current
        capacity.
        """
        raw = self._call('GET', 'capacity')
        return Capacity.parse_raw(raw)

    def info(self) -> Info:
        """Sends a request to retrieve information about server
        """
        raw = self._call('GET', 'info')
        return Info.parse_raw(raw)

    def ping(self) -> Pong:
        """Sends ping request
        """
        raw = self._call('GET', 'ping')
        return Pong.parse_raw(raw)

    def _mk_url(self, url_parts: Tuple[str, ...]):
        # TODO: use urllib to construct the url.
        return '/'.join((self._api_address,) + url_parts)

    def _call(self, method: str, *url_parts, data=None,
              params=None, stream=None) -> bytes:
        """Sends a request with given method, url, data, params to the
        specified server address.

        Parameters:
          method: a request method
          url_parts: request URL parts
          data: data to be sent
          params: params to be sent
          stream: flag

        Raises:
          APIError: when something wrong with a response.
        """
        response = self.request(method.upper(),
                                self._mk_url(url_parts),
                                params=params,
                                data=data,
                                stream=stream)

        if response.status_code not in (200, 201):
            try:
                self._raise_error(response.status_code, response.json())
            except ValueError:
                raise APIError(response.status_code,
                               self._RESPONSE_NOT_JSON_MSG)

        return response.content

    def _raise_error(self, status: int, result: dict):
        """Raises an error with given status and data.

        Parameters:
          status: a response status
          result: a parsed response result
        Raises:
          APIError: always raises that exception.
        """
        raise APIError(status, self._get_error_text(result))

    def _get_error_text(self, result: dict) -> str:
        """Returns an error text.

        Parameters:
          result: a result dictionary.
        """
        try:
            return result[self._FIELD_TEXT]
        except KeyError:
            return self._DEFAULT_ERROR_MSG


__all__ = [
    'APIClient',
    'APIError',
    'SORTING_SMART',
    'SORTING_RANDOM',
]
