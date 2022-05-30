import json
import jwt
import uuid
from copy import deepcopy
import random

import const
import token_mgr
from utils import log, mysqlDB, httpserver, tools, exception

# 登录错误缓存区大小
MAX_LRU_COUNT_NUM = 10000
# 统计登录出错次数
global g_login_failed
g_login_failed = tools.LRUCache(MAX_LRU_COUNT_NUM)
# 缓存验证码
global g_captcha_array
g_captcha_array = {}
# 每一个验证码的有效期为2分钟
VALIDITY_TIME = 2 * 60
# 超时多久后删除验证码
CAPTCHA_DELETE_TIME = 5 * 60


@exception.exception_handler('contract')
async def _login(request):
    log.logger.info("------login start-------------")
    state = True
    result = True
    body = {}
    auth_dict = json.loads(await request.text())
    log.logger.info(auth_dict)
    username = auth_dict.get('username')
    password = auth_dict.get('psd')
    uuid = auth_dict.get('uuid')
    if username is None or password is None:
        log.logger.info('user name or password is None')
        body = deepcopy(const.ERRORMSG['INPUT_NULL_ERR'])
        body['result'] = False
        return httpserver.web_response(True, body)

    # 验证用户名密码
    sql = "select id,username,psd,phone,email,salt from user where username = %s;"

    args = (username,)
    enter_info_reslut = await mysqlDB.db_select(sql, args=args)
    enter_info_dict = {}
    permission = {}
    log.logger.info(enter_info_reslut)
    if enter_info_reslut is None or len(enter_info_reslut) != 1:
        body = deepcopy(const.ERRORMSG['USER_INFO_ERR'])
        body['result'] = False
        return httpserver.web_response(True, body)
    else:
        # 将输入密码与slathash后，与数据库的比较
        enter_info_dict = enter_info_reslut[0]
        id = enter_info_dict['id']
        hash_passwd = tools.get_hash(password, enter_info_dict['salt'])
        if enter_info_dict['psd'] != hash_passwd:
            log.logger.error("get hash error")
            body = deepcopy(const.ERRORMSG['USER_INFO_ERR'])
            body['result'] = False
            return httpserver.web_response(True, body)
        else:
            del enter_info_dict['psd']
            del enter_info_dict['salt']
            result = True
        body['result'] = result

    # 生成token
    payload = {"permission": permission, "enterinfo": enter_info_dict}
    token = token_mgr.gen_token(payload)
    body['token'] = token
    body['id'] = id
    body['username'] = username
    log.logger.info("--------------login end---------------")
    return httpserver.web_response(state, body)



@exception.exception_handler('contract')
async def _logout(request):
    req_dict = json.loads(await request.text())
    log.logger.info("_logout is begin! req_dict = {0}".format(req_dict))
    token = req_dict.get('token')
    decoded = jwt.decode(token, '123456',algorithms='HS256',verify_signature=False)
    token_mgr.rm_token(decoded)
    body = {'result': True}
    body.update(decoded)
    log.logger.info("_logout is end!")
    return httpserver.web_response(True, body)


@exception.exception_handler('contract')
async def _sign_up(request):
    req_dict = json.loads(await request.text())
    log.logger.info("_sign_up is begin! {0}".format(req_dict))
    username = req_dict.get('username')
    email = req_dict.get('email') if req_dict.get('email') else ''
    body = {}
    sql = "select id from user where username=%s or email=%s;"
    args = (username, email)
    result = await mysqlDB.db_select(sql, args)
    if len(result) == 0:
        psd = req_dict.get('psd')
        phone = req_dict.get('phone') if req_dict.get('phone') else ''
        salt = str(uuid.uuid1()).replace('-', '')
        hash_passwd = tools.get_hash(psd, salt)
        sql = "INSERT INTO user (username, psd, phone, email, salt) VALUES (%s, %s, %s, %s, %s);"
        args = (username, hash_passwd, phone, email, salt)
        await mysqlDB.db_exec(sql, args)
    else:
        body = const.ERRORMSG['INPUT_EXISTS_ERR']
        body['result'] = False
        return httpserver.web_response(False, body)

    body['result'] = True
    return httpserver.web_response(True, body)


@exception.exception_handler('contract')
async def _reset_psd(request):
    req_dict = json.loads(await request.text())
    log.logger.info("_sign_up is begin! {0}".format(req_dict))
    email = req_dict.get('email')
    body = {}
    sql = "select id from user where email=%s;"
    args = (email,)
    result = await mysqlDB.db_select(sql, args)
    if len(result) == 0:
        body = const.ERRORMSG['EMAIL_NOT_EXIST_ERR']
        body['result'] = False
        return httpserver.web_response(False, body)
    else:
        psd = req_dict.get('psd')
        salt = str(uuid.uuid1()).replace('-', '')
        hash_passwd = tools.get_hash(psd, salt)
        sql = "update user set psd=%s, salt=%s where email=%s;"
        args = (hash_passwd, salt, email)
        await mysqlDB.db_exec(sql, args)

    body['result'] = True
    return httpserver.web_response(True, body)


def add_route(webapp):
    # webapp.router.add_route('POST', '/get_permission', _get_permission)
    webapp.router.add_route('POST', '/login', _login)
    webapp.router.add_route('POST', '/logout', _logout)
    webapp.router.add_route('POST', '/signup', _sign_up)
    webapp.router.add_route('POST', '/reset_psd', _reset_psd)
