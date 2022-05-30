# encoding=utf-8
import jwt
import json
from aiohttp import web

import token_mgr
from utils import log
# from oplog import _oplog


class Http:
    def __init__(self, ip, port, func, middlewares=(), loop=None):
        self._loop = loop
        if middlewares is not None:
            middlewares = list(middlewares)
        else:
            middlewares = []
        middlewares.append(_jwt_decode_factory)
        # middlewares.append(_oplog)
        self._app = web.Application(
            loop=loop, middlewares=middlewares, client_max_size=1024**100)
        # self._app.on_response_prepare.append(_oplog)
        self._server = None
        self._ip = ip
        self._port = port
        func(self._app)

    def start(self):
        self._handler = self._app.make_handler()
        self._server = self._loop.create_server(self._handler, self._ip,
                                                self._port)

    async def stop(self):
        self._server.close()
        await self._server.wait_closed()
        await self._app.shutdown()
        await self._handler.shutdown()
        await self._app.cleanup()


# async def _check_method(app, handler):
#     log.logger.info("check method start...")
#
#     async def middleware(request):
#         request.headers
#         url_ = str(request.url)
#         log.logger.info("_jwt_decode_factory url={0}".format(url_))
#         if 'login' in url_ or 'signup' in url_:
#             return await handler(request)
#         vaild = False
#         if 'Authorization' in request.headers:
#             token = None
#             try:
#                 scheme, token = request.headers.get(
#                     'Authorization').strip().split(' ')
#                 log.logger.info("_jwt_decode_factory scheme={0}, token={1}".format(scheme, token))
#                 if scheme == 'Bearer':
#                     decoded = jwt.decode(token, '123456', algorithms='HS256', verify_signature=False)
#                     log.logger.info("decoded info={0}".format(decoded))
#                     # decoded = jwt.decode(token, verify=False)
#                     request['decodedToken'] = decoded
#                     refresh = token_mgr.refresh_token(decoded)
#                     if refresh:
#                         vaild = True
#             except Exception as e:
#                 log.logger.info(e)
#         if vaild:
#             return await handler(request)
#         else:
#             return web_response(
#                     False, {
#                         "errorCode": 10050998,
#                         "errorMessage": "当前会话已过期，请重新登录。"
#                     })
#     return middleware


async def _jwt_decode_factory(app, handler):
    log.logger.info("_jwt_decode_factory start...")

    async def middleware(request):
        url_ = str(request.url)
        if request.method=='GET':
            return await handler(request)
        log.logger.info("header:{}".format(request.method))
        log.logger.info("_jwt_decode_factory url={0}".format(url_))
        if 'login' in url_ or 'signup' in url_ or 'process_img' in url_ or 'reset_psd' in url_ or 'upload_model' in url_:
            return await handler(request)
        vaild = False
        if 'Authorization' in request.headers:
            token = None
            try:
                scheme, token = request.headers.get(
                    'Authorization').strip().split(' ')
                log.logger.info("_jwt_decode_factory scheme={0}, token={1}".format(scheme, token))
                if scheme == 'Bearer':
                    decoded = jwt.decode(token, '123456', algorithms='HS256', verify_signature=False)
                    log.logger.info("decoded info={0}".format(decoded))
                    # decoded = jwt.decode(token, verify=False)
                    request['decodedToken'] = decoded
                    refresh = token_mgr.refresh_token(decoded)
                    if refresh:
                        vaild = True
            except Exception as e:
                log.logger.info(e)
        if vaild:
            return await handler(request)
        else:
            return web_response(
                    False, {
                        "errorCode": 10050998,
                        "errorMessage": "当前会话已过期，请重新登录。"
                    })
    return middleware


def get_decoded_token(request):
    return request.get('decodedToken')


def init(ip, port, func, loop, middlewares=()):
    httpserver = Http(ip, port, func, middlewares, loop=loop)
    httpserver.start()
    return httpserver._server


def web_response(state, body):
    result_dict = {}
    result_dict['success'] = state
    result_dict['content'] = body

    json_str = json.dumps(result_dict)
    return web.Response(body=json_str, content_type='application/json')
