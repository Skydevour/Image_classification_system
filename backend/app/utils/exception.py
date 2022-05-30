import traceback
from functools import wraps

from utils import log, httpserver, httpclient, config


def exception_handler(*param):
    def handler(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except Exception as e:
                return await handle_error(e, function.__name__, param)

        return wrapper

    return handler


async def handle_error(e, func_name, *param):
    log.logger.error("handle_error traceback = {0}".format(
        traceback.format_exc()))
    server_name = []
    error = str(e)
    if len(error) > 100:
        # error信息太长，只需要取最后一行记录
        error_s = error.strip().split('\n')
        error = error_s[-1]
    log.logger.info("handle_error error = {0}".format(error))
    log.logger.info("handle_error param = {0}".format(param[0][0]))
    module = '{0}-{1}'.format(param[0][0], func_name)

    # app 消息推送
    message = "严重：模块{0}出现系统错误{1}，请及时处理。".format(module, error)
    eid_list = [8004, 8012, 8005, 8013]
    req = {
        'message': message,
        'eid_list': eid_list,
        'title': module,
        'type': 899
    }

    return httpserver.web_response(False, {
        "errorCode": 10001999,
        "errorMessage": "系统繁忙，请稍后再试"
    })
