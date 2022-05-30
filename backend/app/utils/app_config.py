# -*- coding: UTF-8 -*-
"""
配置文件定义。
auther: jacob
date:2019-12-09
"""
from utils import database, log, config

CRM_MGR_RECEIVER_REALEASE_EID = {
    'rain': '8000',
    'kevin': '9002',
    'fred': '9001'
}
CRM_MGR_RECEIVER_DEBUG_EID = {}


def get_crm_mgr_receiver_eid(release):
    if release:
        return CRM_MGR_RECEIVER_REALEASE_EID.values()
    else:
        return CRM_MGR_RECEIVER_DEBUG_EID.values()


async def _get_related_cid(eid_list):
    log.logger.info(
        "_get_related_cid cid_list start eid_list = {0}".format(eid_list))
    if not eid_list or len(eid_list) == 0:
        return []
    sql = "select cid from enter_cidinfo where eid in %s;"
    cid_list = await database.db_select(sql, (eid_list, ))
    log.logger.info("_get_related_cid cid_list = {0} ".format(cid_list))
    return cid_list


async def _get_leads_related_eid(release, id_type, id):
    if id_type == 'eid':
        sql = "select mgr_eid, province from {}.gh_leads_info_tbl where eid = %s limit 1;".format(
            database.CRM)
    elif id_type == 'leads_id':
        sql = "select mgr_eid, province from {}.gh_leads_info_tbl where id = %s;".format(
            database.CRM)
    else:
        return []
    res = await database.db_select(sql, (id, ))
    related_mgr_eid = []
    if not res:
        return []
    related_mgr_eid.append(res[0]['mgr_eid'])
    region = config.province_to_region.get(res[0]['province'])
    sql = "select eid, leader_eid from observer_priv where eid=%s or (leader=1 and region & %s);"
    log.logger.info("sql_for_related_phone:{},args:{}".format(
        sql, (res[0]['mgr_eid'], region)))
    ress = await database.db_select(sql, (res[0]['mgr_eid'], region))
    if ress:
        for item in ress:
            if item['eid'] and item['eid'] not in related_mgr_eid:
                related_mgr_eid.append(item['eid'])
            if item['leader_eid'] and item['leader_eid'] not in related_mgr_eid:
                related_mgr_eid.append(item['leader_eid'])
    related_mgr_eid.remove(res[0]['mgr_eid'])
    if len(related_mgr_eid) == 0:
        return []
    # sql = "select phone from enter_info_tbl where eid in %s;"
    # phones = await database.db_select(sql, (related_mgr_eid, ))
    # if not phones:
    # return []
    # phones = [x['phone'] for x in phones]
    # log.logger.info("related_phones:{}".format(phones))
    if not release:
        log.logger.info("debug mode,return:{}".format([8005]))
        return [8005]
    return related_mgr_eid
