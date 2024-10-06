import logging

from utils.settings import current_settings

api_logger = logging.getLogger('api_logs')
api_logger.setLevel(current_settings.log_level)

ch = logging.StreamHandler()
ch.setLevel(current_settings.log_level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
api_logger.addHandler(ch)

