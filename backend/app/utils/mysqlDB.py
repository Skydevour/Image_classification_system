import asyncio
import aiomysql
from async_timeout import timeout
import traceback
import datetime
from utils import log
from utils import decorator

SQL_CFG_RELEASE = [{
    # 'host': '172.16.1.143',
    # 'port': 3306,
    # 'username': 'root',
    # 'passwd': '12345678',
    # 'database': 'fee'
}]
SQL_CFG_DEBUG = [{
    # 'host': '172.16.1.143',
    # 'port': 3306,
    # 'username': 'root',
    # 'passwd': '12345678',
    # 'database': 'fee'
}]

MIN_CONN_SIZE = 1
MAX_CONN_SIZE = 10
MAX_INDEX = 10000
global db_connection_array
db_connection_array = []
global current_db_cfg
array_index = 0


async def init(db_conf=None, release=False, dbname='fee'):
    global current_db_cfg
    if db_conf is None:
        if release:
            current_db_cfg = SQL_CFG_RELEASE
        else:
            current_db_cfg = SQL_CFG_DEBUG
    else:
        current_db_cfg = db_conf
    log.logger.info(current_db_cfg)
    global db_connection_array
    count = len(current_db_cfg)
    for i in range(0, count):
        db_cfg_dict = current_db_cfg[i]
        # if dbname is not None:
        #     db_cfg_dict['database'] = dbname
        # dbname = db_cfg_dict
        db_connection_dict = {}
        db_connection_dict['host'] = db_cfg_dict['host']
        db_connection_pool = await create_connect_array(db_cfg_dict)
        if db_connection_pool is None:
            continue
        db_connection_dict['db_connection_pool'] = db_connection_pool
        db_connection_array.append(db_connection_dict)
    if len(db_connection_array) == 0:
        raise Exception('db init error: the len(arrays) == 0')


async def create_connect_array(db_dict):
    log.logger.info(db_dict)
    db_connection_pool = None
    try:
        async with timeout(10):
            db_connection_pool = await aiomysql.create_pool(
                minsize=MIN_CONN_SIZE,
                maxsize=MAX_CONN_SIZE,
                host=db_dict['host'],
                user=db_dict['username'],
                password=db_dict['passwd'],
                db=db_dict['database'],
                port=db_dict['port'],
                charset='utf8')
    except asyncio.TimeoutError as e_timeout:
        log.logger.error(e_timeout)
        raise Exception('create pool error :asyncio.TimeoutError time out')
    except Exception as e:
        log.logger.error(e)
        raise Exception(traceback.format_exc())
    return db_connection_pool


async def rebuild_connection(connection_array, db_config_dict):
    is_rebuild_connetion_pool = True
    db_connect_array_count = len(connection_array)
    for j in range(0, db_connect_array_count):
        db_connection_dict = connection_array[j]
        if db_connection_dict['host'] == db_config_dict['host']:
            is_rebuild_connetion_pool = False
            break
    if is_rebuild_connetion_pool is True:
        db_connection_dict = {}
        db_connection_dict['host'] = db_config_dict['host']
        db_connection_pool = await create_connect_array(db_config_dict)
        if db_connection_pool is None:
            return
        db_connection_dict['db_connection_pool'] = db_connection_pool
        connection_array.append(db_connection_dict)


async def rebuild_db_connection():
    global current_db_cfg
    global db_connection_array
    try:
        dbCount = len(current_db_cfg)
        for i in range(0, dbCount):
            db_config_dict = current_db_cfg[i]
            await rebuild_connection(db_connection_array, db_config_dict)
    except Exception as e:
        log.logger.error(e)
        error = traceback.format_exc()
        raise Exception(error)


@decorator.timer(1)
async def rebuild_db_connection_array():
    try:
        await rebuild_db_connection()
    except Exception as e:
        log.logger.error(e)


def get_connection_pool(db_connection_array):

    array_len = len(db_connection_array)
    if array_len == 0:
        return None
    global array_index
    index = array_index % array_len
    array_index += 1
    if array_index > MAX_INDEX:
        array_index = 0
    return db_connection_array[index]


async def delete_pool(db_connection_array, connection_dict):
    if len(db_connection_array) != 0:
        try:
            db_connection_array.remove(connection_dict)
        except Exception as e:
            log.logger.error(e)

    if len(db_connection_array) == 0:
        await rebuild_db_connection()
    return


async def db_select_ex(sql, args=None, out_of_time=5):
    results = None
    error = ''
    global db_connection_array
    connection_dict = get_connection_pool(db_connection_array)
    is_delte_connection_dict = False
    if connection_dict is None:
        return None
    # 创建游标
    connection_pool = connection_dict['db_connection_pool']
    try:
        async with timeout(out_of_time + 1) as cm:
            async with connection_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    async with timeout(out_of_time) as cm:
                        if args is None:
                            await cur.execute(sql)
                        else:
                            await cur.execute(sql, args)
                        results = await cur.fetchall()
                    if cm.expired is True:
                        results = None
                        error = '{0}:query sql time out sql = {1},timeout = {2},connection_dict = {3}'\
                                .format(datetime.datetime.now(), sql, out_of_time, connection_dict)
                        is_delte_connection_dict = True
                    await cur.close()
                    await conn.commit()

    except asyncio.TimeoutError as e_timeout:
        log.logger.error(e_timeout)
        error = '{0}:db_select_ex asyncio.TimeoutError time out sql = {1},timeout = {2},connection_dict = {3}'\
                .format(datetime.datetime.now(), sql, out_of_time, connection_dict)
        is_delte_connection_dict = True

    except Exception as e:
        error = sql + traceback.format_exc()
        err_info = "{0}".format(e)
        if err_info.find('2003') >= 0 or err_info.find(
                '1105') >= 0 or err_info.find('2013') >= 0:
            is_delte_connection_dict = True

    if is_delte_connection_dict is True:
        await delete_pool(db_connection_array, connection_dict)
        results = None
    if error != '':
        raise Exception(error)
    return results


async def db_select(sql, args=None, out_of_time=90):
    result = None
    try:
        result = await db_select_ex(sql, args, out_of_time)
    except Exception as e:
        log.logger.info(e)
        try:
            result = await db_select_ex(sql, args, out_of_time)
        except Exception as e:
            raise Exception(e)
    return result


async def db_exec_ex(sql_str, args=None, out_of_time=90):
    is_delte_connection_dict = False
    error = ''
    global db_connection_array
    connection_dict = get_connection_pool(db_connection_array)
    if connection_dict is None:
        return None
    connection_pool = connection_dict['db_connection_pool']
    try:
        async with timeout(out_of_time + 1):
            async with connection_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    async with timeout(out_of_time) as cm:
                        try:
                            if args is None:
                                await cursor.execute(sql_str)
                            else:
                                await cursor.execute(sql_str, args)
                            await conn.commit()
                            await cursor.close()
                        except Exception as e:
                            error = traceback.format_exc()
                            err_info = "{0}".format(e)
                            if err_info.find('2003') >= 0 or err_info.find(
                                    '1105') >= 0 or err_info.find('2013') >= 0:
                                is_delte_connection_dict = True
                            await cursor.close()
                            await conn.rollback()

                    if cm.expired is True:
                        error = '{0}: db_exec exec sql timeout sql  = {1} connection_dict = {2}'.format(
                            datetime.datetime.now(), sql_str, connection_dict)
                        await cursor.close()
                        await conn.rollback()
                        is_delte_connection_dict = True
    except asyncio.TimeoutError as e_timeout:
        log.logger.error(e_timeout)
        error = '{0}: db_exec asyncio.TimeoutError time out sql  = {1} connection_dict = {2}'.format(
            datetime.datetime.now(), sql_str, connection_dict)
        is_delte_connection_dict = True

    if is_delte_connection_dict is True:
        await delete_pool(db_connection_array, connection_dict)

    if error != '':
        raise Exception(error)


async def db_exec(sql, args=None, out_of_time=90):
    try:
        await db_exec_ex(sql, args, out_of_time)
    except Exception as e:
        log.logger.info(e)
        try:
            await db_exec_ex(sql, args, out_of_time)
        except Exception as e:
            raise Exception(e)
