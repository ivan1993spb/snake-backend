"""The module contains classes and methods to work with the API of
the Snake-Server.
"""

from typing import Any, Tuple

from requests.utils import CaseInsensitiveDict
from requests import Session


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

    def get_games(self, limit: int = None, sorting: str = None) -> Any:
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
        return self._call('GET', 'games', params=params)

    def get_game(self, game_id: int) -> Any:
        """Returns information about a game with specified game identifier.

        Parameters:
          game_id: a game identifier.
        """
        return self._call('GET', 'games', str(game_id))

    def get_game_objects(self, game_id: int) -> Any:
        """Returns information about game objects placed on a game map.

        Parameters:
          game_id: a game identifier.
        """
        return self._call('GET', 'games', str(game_id), 'objects')

    def delete_game(self, game_id: int) -> Any:
        """Sends a request for deleting a game.

        Parameters:
          game_id: a game identifier.
        """
        return self._call('DELETE', 'games', str(game_id))

    def create_game(self, limit: int, width: int, height: int,
                    enable_walls: bool = True) -> Any:
        """Sends a request to create a game with given parameters.

        Parameters:
          limit: players limit.
          width: map width.
          height: map height.
          enable_walls: flag whether to add walls or not.
        """
        return self._call('POST', 'games', data={
            'limit': limit,
            'width': width,
            'height': height,
            'enable_walls': enable_walls,
        })

    def broadcast(self, game_id: int, message: str) -> Any:
        return self._call('POST', 'games', str(game_id), 'broadcast', data={
            'message': message,
        })

    def capacity(self) -> Any:
        """Sends a request to retrieve information about server current
        capacity.
        """
        return self._call('GET', 'capacity')

    def info(self) -> Any:
        """Sends a request to retrieve information about server
        """
        return self._call('GET', 'info')

    def ping(self) -> Any:
        """Sends ping request
        """
        return self._call('GET', 'ping')

    def _mk_url(self, url_parts: Tuple[str, ...]):
        return '/'.join((self._api_address,) + url_parts)

    def _call(self, method: str, *url_parts, data=None,
              params=None, stream=None) -> Any:
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
        result = response.json()
        if response.status_code not in (200, 201):
            self._raise_error(response.status_code, result)
        return result

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
        # TODO: Create an error parser.
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
