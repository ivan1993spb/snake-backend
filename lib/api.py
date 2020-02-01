from requests.utils import CaseInsensitiveDict
from requests import Session


_PARAM_LABEL_LIMIT = 'limit'
_PARAM_LABEL_SORTING = 'sorting'

SORTING_SMART = 'smart'
SORTING_RANDOM = 'random'

_SORTING = (SORTING_SMART, SORTING_RANDOM)


class APIClient(Session):
    _DEFAULT_USER_AGENT = 'SnakeAPIClient'

    def __init__(self, api_address: str, user_agent=None):
        assert api_address.endswith('/api'), 'API address must end with "/api"'

        super().__init__()

        self._api_address = api_address
        self._user_agent = user_agent or self._DEFAULT_USER_AGENT

        self.headers.update(self._initial_headers())

    def _initial_headers(self):
        return CaseInsensitiveDict({
            'User-Agent': self._user_agent,
            'X-Snake-Client': self._user_agent,
            'Accept': 'application/json',
        })

    def get_games(self, limit=None, sorting=None):
        params = {}
        if limit:
            params[_PARAM_LABEL_LIMIT] = limit
        if sorting:
            assert sorting in _SORTING, 'Invalid sorting type has been passed'
            params[_PARAM_LABEL_SORTING] = sorting
        return self._call('GET', 'games', params=params)

    def get_game(self, game_id: int):
        return self._call('GET', 'games', str(game_id))

    def get_game_objects(self, game_id: int):
        return self._call('GET', 'games', str(game_id), 'objects')

    def delete_game(self, game_id: int):
        return self._call('DELETE', 'games', str(game_id))

    def create_game(self, limit: int, width: int, height: int, enable_walls=True):
        return self._call('POST', 'games', data={
            'limit': limit,
            'width': width,
            'height': height,
            'enable_walls': enable_walls,
        })

    def broadcast(self, game_id: int, message: str):
        return self._call('POST', 'games', str(game_id), 'broadcast', data={
            'message': message,
        })

    def capacity(self):
        return self._call('GET', 'capacity')

    def info(self):
        return self._call('GET', 'info')

    def ping(self):
        return self._call('GET', 'ping')

    def _url(self, url):
        return '/'.join((self._api_address,) + url)

    def _call(self, method: str, *url, data=None, params=None, stream=None):
        response = self.request(method.upper(), self._url(url), params=params, data=data, stream=stream)
        return response.json(), response.status_code in (200, 201)


__all__ = [
    'APIClient',
    'SORTING_SMART',
    'SORTING_RANDOM',
]
