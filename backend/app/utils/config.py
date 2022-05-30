# -*- coding: UTF-8 -*-
"""
配置文件定义。
auther: leo
date:2018-06-13
"""
from utils import database

PHONE_NUMBERS_DEBUG = []
JUNSHI_RECEIVER_DEBUG = {}
DB_RECEIVER_DEBUG = {}
GATEWAY_RECEIVER_DEBUG = {}
CONSOLE_RECEIVER_DEBUG = {}
CFG_RECEIVER_DEBUG = {}
CRM_MGR_RECEIVER_DEBUG = {}
CUSTOM_MGR_RECEIVER_DEBUG = {}

WOLONG_IP = "172.16.246.170"
WOLONG_PORT = 19999
REDIS_IP = "172.16.246.170"
REDIS_PORT = 55904
FILES_IP_DEBUG = "localhost"
FILES_IP_REALEASE = "172.16.246.170"
FILES_PORT = 10005
GW_SERVER_IP = "172.16.246.167"
GW_SERVER_PORT = 20000
GW_SERVER_PORT_TJG = 21000
REFERER_IP = "180.76.185.32"
REFERER_PORT = 10006
GATE_IP = '172.16.246.163'
IP138_SERVER_IP = '120.27.247.55'

AUTH_PORT = {'public': 10001}
BIGSCREEN_PORT = {'public': 10003, 'guanduDB': 10003}
SMY_PORT = {'guanduDB': 8888, 'taijiguang': 9888, 'taijizhen': 10888}
CORE_PORT = {'guanduDB': 10000, 'taijiguang': 11000, 'taijizhen': 12000}
FILES_PORT_O = {'public': FILES_PORT}
MESSAGE_PORT = {'public': 10008}
MONITOR_PORT = {'guanduDB': 20001, 'taijiguang': 21001, 'taijizhen': 22001}
OPLOG_PORT = {'public': 10002}
OPERATOR_PORT = {'guanduDB': 10007, 'taijiguang': 11007, 'taijizhen': 12007}
REFERER_PORT_O = {'public': REFERER_PORT}
WOLONG_PORT_O = {
    'guanduDB': WOLONG_PORT,
    'taijiguang': 20999,
    'taijizhen': 21999
}
WORKFLOW_PORT = {'public': 10009}
GROWTHHACKER_PORT = {'crm': 10004}
CONTRACT_PORT = {'fee': 10050}
CONTRACT_PORT = {'parking_manage': 10051}

JUNSHI_RECEIVER_REALEASE = {
    'colin': '13396818294',
    'jay': '18057114066',
    'rain': '13396571336'
}
DB_RECEIVER_REALEASE = {
    'colin': '13396818294',
    'jay': '18057114066',
    'rain': '13396571336'
}
GATEWAY_RECEIVER_REALEASE = {
    'colin': '13396818294',
    'jay': '18057114066',
    'rain': '13396571336'
}
CFG_RECEIVER_REALEASE = {
    'colin': '13396818294',
    'jay': '18057114066',
    'rain': '13396571336',
    'kevin': '13868131310'
}
CRM_MGR_RECEIVER_REALEASE = {
    'rain': '13396571336',
    'kevin': '13868131310',
    'fred': '13516811230'
}

CUSTOM_MGR_RECEIVER_REALEASE = {
    'rain': '13396571336',
    'kevin': '13868131310',
    'fred': '13516811230',
    'freya': '13506719204'
}

CONSOLE_RECEIVER_REALEASE = {
    'colin': '13396818294',
    'jay': '18057114066',
    'rain': '13396571336',
    'leo': '18626886596'
}

province_to_region = {
    # 中西部：8
    '河南': 8,
    '湖北': 8,
    '湖南': 8,
    '四川': 8,
    '贵州': 8,
    '云南': 8,
    '重庆': 8,
    '西藏': 8,
    # 南部：4
    '广东': 4,
    '广西': 4,
    '海南': 4,
    '香港': 4,
    '澳门': 4,
    # 北部：2
    '北京': 2,
    '天津': 2,
    '河北': 2,
    '山西': 2,
    '内蒙古': 2,
    '黑龙江': 2,
    '吉林': 2,
    '辽宁': 2,
    '陕西': 2,
    '甘肃': 2,
    '宁夏': 2,
    '青海': 2,
    '新疆': 2,
    # 东部：1
    '山东': 1,
    '江苏': 1,
    '安徽': 1,
    '上海': 1,
    '浙江': 1,
    '江西': 1,
    '福建': 1,
    '台湾': 1
}


def get_files_ip(release):
    if release:
        return FILES_IP_REALEASE
    else:
        return FILES_IP_DEBUG


def get_crm_mgr_receiver(release):
    if release:
        return CRM_MGR_RECEIVER_REALEASE.values()
    else:
        return CRM_MGR_RECEIVER_DEBUG.values()


async def get_pyhone_numbers(release):
    if release:
        sql = "select phone from enter_info_tbl where eid>=9000 and eid<10000 and state!=-1 and business!=-1 and business!=-2;"
        return_value = await database.db_select(sql)
        numbers = []
        if return_value:
            numbers = [item["phone"] for item in return_value]
        numbers.append("13396571336")
        return numbers
    else:
        return PHONE_NUMBERS_DEBUG


async def get_phone_numbers_when_register(release, eid):
    # 根据线索的不同状态获取特定的电话号码
    # 注册时：线索的销售经理 + 各个区域的leader + Kevin、 Fred、 Rain、Freya
    if release:
        # try:
        #     server_name = await remote.get_server_name()
        #     log.logger.info("server is {}".format(server_name))
        # except Exception as e:
        #     log.logger.error(e)
        #     return []
        # if server_name and 'cns' in server_name:
        #     log.logger.info("crm2 in server_name, return")
        #     return []
        all_phones = []
        for _, phone in CUSTOM_MGR_RECEIVER_REALEASE.items():
            all_phones.append(phone)
        all_leaders_sql = "select eid from observer_priv where leader=1;"
        res = await database.db_select(all_leaders_sql)
        if res:
            all_leaders_eids = tuple([x['eid'] for x in res])
            sql = "select phone from enter_info_tbl where eid in %s;"
            ress = await database.db_select(sql, (all_leaders_eids, ))
            if ress:
                for item in ress:
                    all_phones.append(item.get('phone'))

        releated_phones = await _get_leads_related_phones(
            release=release, id_type='eid', id=eid)
        all_phones += releated_phones
        return list(set(all_phones))
    else:
        return list(CUSTOM_MGR_RECEIVER_DEBUG.values())


def get_db_receiver(release):
    if release:
        return DB_RECEIVER_REALEASE.values()
    else:
        return DB_RECEIVER_DEBUG.values()


def get_junshi_receiver(release):
    if release:
        return JUNSHI_RECEIVER_REALEASE.values()
    else:
        return JUNSHI_RECEIVER_DEBUG.values()


def get_gateway_receiver(release):
    if release:
        return GATEWAY_RECEIVER_REALEASE.values()
    else:
        return GATEWAY_RECEIVER_DEBUG.values()


def get_cfg_receiver(release):
    if release:
        return CFG_RECEIVER_REALEASE.values()
    else:
        return CFG_RECEIVER_DEBUG.values()


def get_console_receiver(release):
    if release:
        return CONSOLE_RECEIVER_REALEASE.values()
    else:
        return CONSOLE_RECEIVER_DEBUG.values()
