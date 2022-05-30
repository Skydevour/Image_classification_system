import hashlib
import pickle
import random
import string
import os
import sys
import traceback
from collections import OrderedDict
from utils import log, httpclient, database


def getArgv(argv):
    if len(argv) != 3:
        log.logger.error("Please input dbname and debug(release).")
        sys.exit(1)
    dbname = argv[1]
    if dbname not in database.DBNAME:
        log.logger.error("Please input dbname and debug(release).")
        sys.exit(1)
    release = False
    if argv[2] == 'release':
        release = True
    elif argv[2] == 'debug':
        release = False
    else:
        log.logger.error("Please input dbname and debug(release).")
        sys.exit(1)
    return dbname, release


def getArgv3(argv):
    if len(argv) != 4:
        log.logger.error(
            "Please input dbname and debug(release) and db_conf path.")
        sys.exit(1)
    dbname = argv[1]
    if dbname not in database.DBNAME:
        log.logger.error(
            "Please input dbname and debug(release) and db_conf path.")
        sys.exit(1)
    release = False
    if argv[2] == 'release':
        release = True
    elif argv[2] == 'debug':
        release = False
    else:
        log.logger.error(
            "Please input dbname and debug(release) and db_conf path.")
        sys.exit(1)
    path = argv[3]
    return dbname, release, path


def get_hash(src, salt):
    key = "{0}{1}".format(src, salt)
    m = hashlib.sha256()
    m.update(key.encode(encoding='utf_8'))
    return m.hexdigest()


# 生成4位数字验证码
def create_check_code():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    x = random.choice(chars), random.choice(chars), random.choice(
        chars), random.choice(chars), random.choice(chars), random.choice(
            chars)
    code = "".join(x)
    return code



def send_sms_by_yunpian(tpl_id, tpl_value, phones):
    if not phones or len(phones) == 0:
        return False
    send_msg_yunpian.sms_put(tpl_id, tpl_value, phones)
    return True


def store_obj(obj, path):
    '''
    store object to path as binary file
    '''
    try:
        with open(path, 'wb') as f:
            pickle.dump(obj, f)
            return
    except Exception:
        log.logger.error('store object error: {0}'.format(
            traceback.format_exc()))

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
        log.logger.error('restore object error:{0}'.format(
            traceback.format_exc()))
    try:
        log.logger.info("rename {0} to {1}".format(path, path + "-bak"))
        os.rename(path, path + "-bak")
        return None
    except Exception:
        log.logger.error('rename error: {0}'.format(traceback.format_exc()))


def gen_password(length):
    # 随机出数字的个数
    num_of_num = random.randint(1, length - 1)
    num_of_letter = length - num_of_num
    # 选中num_of_num个数字
    slc_num = [random.choice(string.digits) for i in range(num_of_num)]
    # 选中num_of_letter个字母
    slc_letter = [
        random.choice(string.ascii_letters) for i in range(num_of_letter)
    ]
    # 打乱这个组合
    slc_char = slc_num + slc_letter
    random.shuffle(slc_char)
    # 生成密码
    gen_pwd = ''.join([i for i in slc_char])
    return gen_pwd


async def save_ipregion(ip):
    province, city, tel_opt, overseas, _, _, _ = await ip_region_thread.save_ipregion_by_source(
        ip, 'ip2region')
    ip_region_thread.ipplus_push(ip)
    ip_region_thread.ibsamap_push(ip)
    return province, city, tel_opt, overseas


async def get_city_by_ip(ipValue):
    city = ""
    try:
        url = 'http://api.ip138.com/query/?ip=%s&datatype=jsonp&token=a43848933bc4c57d09d4e25857f62ea1' % ipValue
        state, resp = await httpclient.request_get(url)
        log.logger.info("state:{0}  resp:{1}".format(state, resp))
        if state and resp.get('ret') == 'ok':
            ipLocation = resp.get('data')
            if (ipLocation is not None and len(ipLocation) >= 3):
                province = ipLocation[1]
                city = ipLocation[2]
                if (city is None or len(city) == 0):
                    country = ipLocation[0]
                    if ("中国" != country):
                        # 如果没有城市，而且不是中国，直接显示国家信息
                        city = country or "未知"
                    else:
                        # 如果没有城市，取省份。 省份也没有，则为未知
                        if (province is None or len(province) == 0):
                            city = "未知"
                        else:
                            city = province
                else:
                    # 北京，上海之类的直辖市
                    if (city != province):
                        city = province + "-" + city
            else:
                log.logger.error("get ip location is None")
        else:
            log.logger.error("get ip location failed")
    except Exception as e:
        log.logger.error("get_city_by_ip error : {0}".format(e))
    log.logger.error("get_city_by_ip city = {0}".format(city))
    return city


async def get_overseas_status_by_ip(ipValue):
    city = ""
    try:
        url = 'http://api.ip138.com/query/?ip=%s&datatype=jsonp&token=a43848933bc4c57d09d4e25857f62ea1' % ipValue
        state, resp = await httpclient.request_get(url)
        log.logger.info("state:{0}  resp:{1}".format(state, resp))
        if state and resp.get('ret') == 'ok':
            ipLocation = resp.get('data')
            if (ipLocation is not None and len(ipLocation) >= 3):
                province = ipLocation[1]
                city = ipLocation[2]
                if (city is None or len(city) == 0):
                    country = ipLocation[0]
                    if ("本地局域网" == country):
                        return 0
                    elif ("保留地址" == country):
                        return 0

                    if ("中国" != country):
                        # 如果没有城市，而且不是中国，直接显示国家信息
                        return 1
                    else:
                        # 如果没有城市，取省份。 省份也没有，则为未知
                        if (province is None or len(province) == 0):
                            return 0
                        elif ("香港" == province):
                            return 1
                        else:
                            return 0
                else:
                    # 北京，上海之类的直辖市
                    if ("香港" == province):
                        return 1
                    if ("香港" == city):
                        return 1
                    else:
                        return 0
            else:
                log.logger.error("get ip location is None")
        else:
            log.logger.error("get ip location failed")
    except Exception as e:
        log.logger.error("get_city_by_ip error : {0}".format(e))
    log.logger.error("get_city_by_ip city = {0}".format(city))
    return -1


class LRUCache(OrderedDict):
    capacity = 0
    cache = None

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if self.cache.get(key):
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            value = None

        return value

    def set(self, key, value):
        if self.cache.get(key):
            value = self.cache.pop(key)
            self.cache[key] = value
        else:
            if len(self.cache) == self.capacity:
                self.cache.popitem(last=False)  # pop出第一个item
                self.cache[key] = value
            else:
                self.cache[key] = value

    def pop(self, key):
        if self.cache.get(key) is not None:
            self.cache.pop(key)

    def get_length(self):
        return len(self.cache)


def file_md5(filepath):
    try:
        if os.path.exists(filepath) is False:
            return None
        with open(filepath, mode='rb') as f:
            content = f.read()
            md5 = hashlib.md5()
            md5.update(content)
            hash = md5.hexdigest()
            return hash
    except Exception:
        log.logger.error(traceback.format_exc())
        return None


# if __name__ == '__main__':
#     import asyncio
#     import uvloop
#     # import database
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(database.init())
#     loop.run_until_complete(get_city_by_ip2region('42.120.75.136'))
