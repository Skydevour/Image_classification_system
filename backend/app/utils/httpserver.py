# encoding=utf-8

import jwt
import json
from aiohttp import web


class Http:
    def __init__(self, ip, port, func, middlewares=(), loop=None):
        self._loop = loop
        if middlewares is not None:
            middlewares = list(middlewares)
        else:
            middlewares = []
        middlewares.append(_jwt_decode_factory)
        self._app = web.Application(
            loop=loop, middlewares=middlewares, client_max_size=1024**100)
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


async def _jwt_decode_factory(app, handler):
    async def middleware(request):
        if 'Authorization' in request.headers:
            token = None
            try:
                scheme, token = request.headers.get(
                    'Authorization').strip().split(' ')
                if scheme == 'Bearer':
                    decoded = jwt.decode(token, verify=False)
                    request['decodedToken'] = decoded
            except Exception as e:
                print(e)
        return await handler(request)

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
