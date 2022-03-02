import logging

from datetime import datetime
from configs import LOG_FILE


logger = logging.getLogger()
handler = logging.FileHandler(LOG_FILE)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log(message):
    timestamp = datetime.today().strftime('%y-%m-%d %H:%M:%S')
    logger.info(f'[{timestamp}] {message}')
