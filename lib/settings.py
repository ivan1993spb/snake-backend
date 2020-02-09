"""Settings module
"""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

from environs import Env


env = Env()
env.read_env()

UNIT_TESTS = env.bool('UNIT_TESTS', False)

DEBUG = env.bool('DEBUG', default=False)

LOG_LEVEL = env.log_level('LOG_LEVEL', 'INFO')

BROKER_REDIS_URL = env('BROKER_REDIS_URL', 'redis://127.0.0.1:6379/0')
RESULT_REDIS_URL = env('RESULT_REDIS_URL', 'redis://127.0.0.1:6379/1')
RATE_LIMITS_REDIS_URL = env('RATE_LIMITS_REDIS_URL', 'redis://127.0.0.1:6379/2')

SNAKE_API_ADDRESS = env('SNAKE_API_ADDRESS', 'http://localhost:8080/api')
CLIENT_NAME = env('CLIENT_NAME', 'SnakeCLIClient')

TASK_INTERVAL_SCREENSHOT = env.int('TASK_INTERVAL_SCREENSHOT', 60)
TASK_INTERVAL_DELETE_CACHE = env.int('TASK_INTERVAL_DELETE_CACHE', 3600)

# Screenshot generation settings

SCREENSHOT_QUALITY = env.int('QUALITY', 70)

SCREENSHOT_SLUG_TINY = 'tiny'
SCREENSHOT_SLUG_SMALL = 'small'
SCREENSHOT_SLUG_MEDIUM = 'medium'
SCREENSHOT_SLUG_BIG = 'big'

SCREENSHOT_LENGTHS = {
    SCREENSHOT_SLUG_TINY: 150,
    SCREENSHOT_SLUG_SMALL: 300,
    SCREENSHOT_SLUG_MEDIUM: 500,
    SCREENSHOT_SLUG_BIG: 700,
}

SCREENSHOT_STRICT_SIZED = env.bool('SCREENSHOT_STRICT_SIZED', True)

SCREENSHOT_DEST_PATH = env('SCREENSHOT_DEST_PATH', 'output/screenshots')

SCREENSHOTS_JSON_FILE = 'report.json'
