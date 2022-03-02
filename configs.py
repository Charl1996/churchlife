from pathlib import Path
from secrets import *

APPLICATION_ROOT_PATH = Path().resolve(__file__).parent

""" ======== FastAPI Web ======== """
APPLICATION_HOST = '127.0.0.1'
APPLICATION_PORT = 8082


""" ======== MESSAGING ======== """
DEFAULT_MESSAGING_HANDLER = 'respondio'


""" ======== SERVICES ======== """
# RabbitMQ
RABBIT_PORT = 5672
BROKER_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASS}@localhost:{RABBIT_PORT}//'


""" ======== LOGGING ======== """
LOGGING_PATH = f'{APPLICATION_ROOT_PATH}/logs/'
LOG_FILE = f'{LOGGING_PATH}/web.log'

