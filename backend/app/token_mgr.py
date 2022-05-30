import jwt
import datetime

from utils import tools, log

global token_infos
token_infos = {}

TOKEN_EXPIRE_TIME = 30 * 60


def gen_token(payload):
    payload['jwtid'] = tools.gen_password(16)
    secret = tools.gen_password(16)
    now = datetime.datetime.now()
    token_info = {'secret': secret, 'refresh_time': now, 'create_time': now}
    if (payload.get('enterinfo')):
        token_info['id'] = payload.get('enterinfo')['id']
        token_info['username'] = payload.get('enterinfo')['username']
    token_info['payload'] = payload
    print(payload)
    global token_infos
    token_infos[payload.get('jwtid')] = token_info
    return jwt.encode(payload, '123456', algorithm='HS256')
    # return jwt.encode(payload, secret)


def refresh_token(decode_token):
    log.logger.info('refresh_token start...')
    jwtid = decode_token.get('jwtid')
    global token_infos
    token = token_infos.get(jwtid)
    if token:
        now = datetime.datetime.now()
        refresh_time = token.get('refresh_time')
        if ((now - refresh_time).seconds > TOKEN_EXPIRE_TIME):
            del token_infos[jwtid]
            return False
        else:
            token['refresh_time'] = now
            return True
    else:
        return False


def rm_token(decode_token):
    log.logger.info('rm_token start...')
    jwtid = decode_token.get('jwtid')
    global token_infos
    token = token_infos.get(jwtid)
    if token:
        del token_infos[jwtid]


async def token_expire():
    log.logger.info("token_expire....")
    global token_infos
    # log.logger.info(token_infos)
    now = datetime.datetime.now()
    keys = token_infos.keys()
    for jwtid in keys:
        token = token_infos[jwtid]
        refresh_time = token.get('refresh_time')
        # log.logger.info(jwtid)
        # log.logger.info(token)
        # log.logger.info((now - refresh_time).seconds)
        if ((now - refresh_time).seconds > TOKEN_EXPIRE_TIME):
            del token_infos[jwtid]
