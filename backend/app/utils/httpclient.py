import aiohttp
# import asyncio
import json
# import uvloop
from utils import log

_addition_headers = {}


def add_product_header(pro):
    _addition_headers['cd-product'] = pro


async def request(url, body={}, headers={}):
    try:
        async with aiohttp.ClientSession() as session:
            xheaders = {**_addition_headers, **headers}
            async with session.post(url, json=body, headers=xheaders) as resp:
                value = await resp.text()
                if resp.status == 200:
                    return (True, json.loads(value))
                else:
                    return (False, {})
    except Exception as e:
        log.logger.error("http request error : {0}".format(e))
        return (False, {})


async def request_form(url, body=None, headers={}):
    try:
        async with aiohttp.ClientSession() as session:
            xheaders = {**_addition_headers, **headers}
            async with session.post(url, data=body, headers=xheaders) as resp:
                value = await resp.text()
                # print(value)
                # print(resp)
                return True, json.loads(value)
                # if resp.status == 200:
                #     return (True, json.loads(value))
                # else:
                #     return (False, json.loads(value))
    except Exception as e:
        log.logger.error("http request error : {0}".format(e))
        return (False, {})


async def request_get(url, params={}):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url, params=params, headers=_addition_headers) as resp:
                value = await resp.text()
                # log.logger.info("status={0}, text = {1}".format(resp.status, value))
                if resp.status == 200:
                    return (True, json.loads(value))
                else:
                    return (False, {})
    except Exception as e:
        log.logger.error("http request error : {0}".format(e))
        return (False, {})


async def request_get_ipserver(url, params={}):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url, params=params, headers=_addition_headers) as resp:
                if resp.status == 200:
                    return True
                else:
                    return False
    except Exception as e:
        log.logger.error("http request error : {0}".format(e))
        return False
