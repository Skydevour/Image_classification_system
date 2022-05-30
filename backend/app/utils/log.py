import logging
import logging.handlers
import os
logger = logging.getLogger("mylog")
LEVEL_DEBUG = logging.DEBUG
LEVEL_INFO = logging.INFO
LEVEL_WARN = logging.WARN
LEVEL_ERROR = logging.ERROR


def log_init(dbname, level=LEVEL_DEBUG):
    log_path = "./{0}_log".format(dbname)
    try:
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
    except Exception as e:
        print(e)
    logger.setLevel(level)
    maxByte = 50 * 1024 * 1024
    fh = logging.handlers.RotatingFileHandler(
        './{0}/log.log'.format(log_path), maxBytes=maxByte, backupCount=100, encoding='utf-8')
    fh.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s %(lineno)d %(levelname)s:  %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
