import logging

from configs import LOG_FILE

logger = logging.getLogger('Web')
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s')

handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.INFO)
