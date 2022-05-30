import pickle
import traceback
import os
from utils import log


def store_obj(obj, path):
    '''
    store object to path as binary file
    '''
    try:
        with open(path, 'wb') as f:
            pickle.dump(obj, f)
            return
    except Exception:
        log.logger.error('store object error: {0}'.format(traceback.format_exc()))

    try:
        os.rename(path, path + "-bak")
    except Exception:
        log.logger.error('rename error: {0}'.format(traceback.format_exc()))


def restore_obj(path):
    '''
    restore from file of path to object
    '''
    try:
        if os.path.exists(path) is not True:
            return
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            return obj
    except Exception:
        log.logger.error("restore error: {0}".format(traceback.format_exc()))

    try:
        log.logger.info("rename {0} to {1}".format(path, path + "-bak"))
        os.rename(path, path + "-bak")
        return None
    except Exception:
        log.logger.error("rename error:{0}".format(traceback.format_exc()))