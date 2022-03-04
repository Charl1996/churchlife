from pathlib import Path
import configparser


configs = configparser.ConfigParser()
configs.read('secrets.ini')


APPLICATION_ROOT_PATH = Path().resolve(__file__)

""" ======== FastAPI Web ======== """
APPLICATION_HOST = configs['application']['Host']
APPLICATION_PORT = int(configs['application']['Port'])


""" ======== DATABASE MANAGER ======== """
DEFAULT_DATABASE_HANDLER = 'breeze'
BREEZE_BASE_URL = configs['breeze']['BaseUrl']
BREEZE_API_KEY = configs['breeze']['ApiKey']


""" ======== MESSAGING ======== """
DEFAULT_MESSAGING_HANDLER = 'respondio'
RESPONDIO_BASE_URL = configs['respond.io']['BaseUrl']
RESPONDIO_API_KEY = configs['respond.io']['ApiKey']


""" ======== LOGGING ======== """
LOGGING_PATH = f'{APPLICATION_ROOT_PATH}/logs/'
LOG_FILE = f'{LOGGING_PATH}/web.log'
CELERY_LOG_FILE = f'{LOGGING_PATH}/celery.log'


""" ======== SERVICES ======== """
RABBITMQ_URL = configs['rabbitmq']['Url']
