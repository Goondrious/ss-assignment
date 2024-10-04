import logging

from utils.settings import Settings

logger = logging.getLogger('api_logs')
logger.setLevel(Settings.log_level)

ch = logging.StreamHandler()
ch.setLevel(Settings.log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

