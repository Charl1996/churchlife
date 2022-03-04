from pathlib import Path
import configparser


configs = configparser.ConfigParser()
configs.read('secrets.ini')


APPLICATION_ROOT_PATH = Path().resolve(__file__)

""" ======== FastAPI Web ======== """
APPLICATION_HOST = configs['application']['host']
APPLICATION_PORT = configs['application']['post']


""" ======== DATABASE MANAGER ======== """
DEFAULT_DATABASE_HANDLER = 'breeze'
BREEZE_BASE_URL = configs['breeze']['base_url']
BREEZE_API_KEY = configs['breeze']['api_key']


""" ======== MESSAGING ======== """
DEFAULT_MESSAGING_HANDLER = 'respondio'
RESPONDIO_BASE_URL = configs['respond.io']['base_url']
RESPONDIO_API_KEY = configs['respond.io']['api_key']


""" ======== LOGGING ======== """
LOGGING_PATH = f'{APPLICATION_ROOT_PATH}/logs/'
LOG_FILE = f'{LOGGING_PATH}/web.log'
CELERY_LOG_FILE = f'{LOGGING_PATH}/celery.log'


""" ======== SERVICES ======== """
RABBITMQ_URL = configs['rabbitmq']['url']
