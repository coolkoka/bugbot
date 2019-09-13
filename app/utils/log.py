import time
import logging
from logging.handlers import TimedRotatingFileHandler
from os import environ


def log_setup(filename):
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(filename)s [LINE: %(lineno)d]: %(message)s')
    formatter.converter = time.gmtime
    log_handler = TimedRotatingFileHandler(filename=environ.get('LOG_PATH') + '/{filename}'.format(filename=filename),
                                           when='d',
                                           interval=1,
                                           backupCount=10)
    log_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.getLevelName(environ.get('LOG_LEVEL')))
