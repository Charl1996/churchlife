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

POSTGRES_USER = configs['postgres']['Username']
POSTGRES_PASSWORD = configs['postgres']['Password']
POSTGRES_PORT = configs['postgres']['Port']
POSTGRES_DATABASE = configs['postgres']['Database']

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


JWT_SECRET = configs['JWT']['Secret']
JWT_ALGORITHM = configs['JWT']['Algorithm']

JWT_COOKIE = 'churchlife_user_jwt'
