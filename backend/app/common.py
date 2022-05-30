import json
from utils import log, httpserver, mysqlDB, database
import re
import datetime

g_release = False

CONTRACT_STATUS = {
    0: "拟定中",
    1: '会签中',
    2: '签署中',
    3: '审核中',
    4: '执行中',
    5: '已到期',
    6: '终止'
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

CN_NUM = {
    '〇': 0,
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '零': 0,
    '壹': 1,
    '贰': 2,
    '叁': 3,
    '肆': 4,
    '伍': 5,
    '陆': 6,
    '柒': 7,
    '捌': 8,
    '玖': 9,
    '貮': 2,
    '两': 2,
}

CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}

unit = ['', '拾', '佰', '千']
sep = ['', '万', '亿', '兆']
accDigits = list('零壹贰叁肆伍陆柒捌玖')
chDigits = list('零一二三四五六七八九')
digits = list('0123456789')
acc_dict = dict(zip(digits, accDigits))
chn_dict = dict(zip(digits, chDigits))


def four_digit_block(num):
    # fill zeros to make 4-digit blocks
    zero_fill_counter = len(num) % 4
    num = ('0' * (4 - zero_fill_counter) +
           num) if zero_fill_counter != 0 else num

    # split input number to 4-digit blocks
    block_num = len(num) // 4
    block_list = [num[4 * i:4 * (i + 1)] for i in range(block_num)]

    return block_list


def is_number(num):
    regex = re.compile(r"^(-?\d+)(\.\d*)?$")
    if re.match(regex, str(num)):
        return True
    else:
        return False


def convert_num_to_chinese(num, dictionary=acc_dict):
    parts = num.split('.')
    num = parts[0]
    decimal = 0
    if len(parts) > 1:
        decimal = parts[1]
    block_list = four_digit_block(num)
    result = ''
    for blockIndex in range(len(block_list)):
        block = block_list[blockIndex]
        for index in range(len(block)):
            # 转换成大写财务数字，如果最大是十位那壹就省略
            if not (index == 2 and block[index] == '1' and blockIndex == 0):
                result += dictionary[block[index]]
            # 加上单位‘千佰拾’等
            if block[index] != '0':
                result += unit[3 - index]
        # 把多个连续的零合并成一个
        result = re.sub(r'(零+)', r'零', result)
        # 去除两头的零
        result = result.strip('零')
        # 加上4位分隔单位‘万，亿’等
        result += sep[len(block_list) - blockIndex - 1]
    result += '元'
    try:
        log.logger.info(decimal)
        if int(decimal) == 0:
            pass
        else:
            if len(decimal) > 2:
                decimal = decimal[:2]
            parts = list(decimal)
            de_dict = {0: '角', 1: '分'}
            for i, x in enumerate(parts):
                result += (dictionary[x] + de_dict[i])
    except Exception as identifier:
        log.logger.info(identifier)
    return result


def chinese_to_arabic(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


def get_release():
    global g_release
    return g_release


def set_release(release):
    global g_release
    g_release = release


async def get_enterprice_info(request):
    decoded_token = httpserver.get_decoded_token(request)
    log.logger.info("decoded_token = {0}".format(decoded_token))
    eid = None
    cross_enterprice = -1
    if decoded_token:
        permission = decoded_token['permission']
        einfo = decoded_token['enterinfo']
        if einfo:
            eid = einfo['eid']
        else:
            log.logger.error(
                "einfo is none. by decoden_token = {0}".format(decoded_token))
        if permission:
            cross_enterprice = permission.get('crossenterprice')
        else:
            log.logger.error(
                "permission is none. by decoden_token = {0}".format(
                    decoded_token))
        data = json.loads(await request.text())
        if cross_enterprice == 1:
            target_eid = data.get('targetEid')
            eid = target_eid if target_eid is not None else eid
            log.logger.info('eid={0}, cross={1}'.format(eid, cross_enterprice))
    else:
        log.logger.error("decoded_token is none")
    log.logger.info('eid={0}, cross={1}'.format(eid, cross_enterprice))
    return eid, cross_enterprice


async def get_usergroup(eid):
    sql_who = "select usergroup from staff_info where eid=%s;"
    res_who = await mysqlDB.db_select(sql_who, (eid, ))
    usergroup = ''
    if res_who and len(res_who) > 0:
        usergroup = res_who[0].get('usergroup')
    return usergroup


async def get_privilege(eid):
    sql_who = "select privilege from staff_info where eid=%s;"
    res_who = await mysqlDB.db_select(sql_who, (eid, ))
    privilege = 0
    if res_who and len(res_who) > 0:
        privilege = res_who[0].get('privilege')
    return privilege


async def get_enter_info(eids):
    enter_info = {}
    if eids:
        sql = "select t2.eid, t2.name, t2.ename, t3.mgr_eid, t3.province as province, t4.username as mgr_name \
            from enter_info_tbl t2, {0}.gh_leads_info_tbl t3, enter_info_tbl t4 \
            where t2.eid in %s and t2.eid=t3.eid and t3.mgr_eid=t4.eid ".format(
            database.CRM)
        args = (tuple(eids), )
        result = await database.db_select(sql, args)
        if result and len(result) > 0:
            for item in result:
                enter_info[item.get('eid')] = item
    return enter_info



def format_under_line_str(linestr, length=30):
    if len(linestr) >= length:
        return linestr
    dif = length - len(linestr)
    left_space = int(dif / 2)
    right_space = dif - left_space
    res = ' ' * left_space + linestr + ' ' * right_space
    return res


async def get_staff_info():
    sql = "select eid, username from staff_info;"
    res = await mysqlDB.db_select(sql)
    data = {}
    if res and len(res) > 0:
        for item in res:
            data[item['eid']] = item['username']
    return data


async def get_privilege_finance_eid():
    sql_get_finance = "select eid from staff_info where privilege&8;"
    res_finance = await mysqlDB.db_select(sql_get_finance)
    eid_finance = 0
    if res_finance and len(res_finance) > 0:
        eid_finance = res_finance[0].get('eid')
    return eid_finance


async def get_privilege_auditor_eid():
    sql_get_auditor = "select eid from staff_info where privilege&4;"
    res_auditor = await mysqlDB.db_select(sql_get_auditor)
    eid_auditor = 0
    if res_auditor and len(res_auditor) > 0:
        eid_auditor = res_auditor[0].get('eid')
    return eid_auditor


async def get_privilege_bm_eids():
    sql_get_bm = "select eid from staff_info where privilege&2;"
    res_bm = await mysqlDB.db_select(sql_get_bm)
    eids_bm = []
    if res_bm and len(res_bm) > 0:
        eids_bm = [x.get('eid') for x in res_bm]
    return eids_bm


# 获取商务经理的电话号码
async def get_bm_phone():
    # 商务经理的权限为privilege的倒数第二位
    sql = "select phone from staff_info where privilege & 2;"
    phones = []
    res = await mysqlDB.db_select(sql)
    if res and len(res) > 0:
        phones = [x.get('phone') for x in res]
    log.logger.info("bm phones:{}".format(phones))
    return phones



def gen_pay_description(number, charge_model, dau_scale, price, payment, cycle,
                        pay_description):
    if number:
        create_year = int(number[4:8])
        create_month = int(number[8:10])
        create_day = int(number[10:12])
        create_time = datetime.date(create_year, create_month, create_day)
    else:
        create_time = datetime.date.today()
    cut_day = datetime.date(2019, 12, 12)
    dau_and_price = ''
    price_description = ''
    payment_description = ''
    if charge_model == 0:
        daus = dau_scale.split(' ')
        prices = price.split(' ')
        if len(daus) != len(prices):
            pass
        else:
            for i in range(len(daus)):
                if daus[i]:
                    temp_text = "日活{}，{}每月;\n".format(
                        daus[i], convert_num_to_chinese(prices[i]))
                    price_description += temp_text
    elif charge_model == 1:
        price_description = "{}每个日活\n".format(
            convert_num_to_chinese(str(price)))
    else:
        price_description = '\n'

    if cycle == '其他' or payment == '其他':
        pass
    else:
        payment_description = '付费方式：'
        if cycle == '月付':
            payment_description += '按月'
        elif cycle == '季付':
            payment_description += '季度'
        elif cycle == '半年付':
            payment_description += '按半年'
        elif cycle == '年付':
            payment_description += '按年'
        if payment == '预付费':
            payment_description += '预付'
        elif payment == '后付费':
            payment_description += '后付'

    if create_time < cut_day:
        if payment == '其他' or cycle == '其他' or charge_model == 2:
            dau_and_price = pay_description
        else:
            dau_and_price = price_description + payment_description
    else:
        # 如果计费模式常规，但另外两项不常规
        if charge_model != 2 and (payment == '其他' or cycle == '其他'):
            dau_and_price = price_description + pay_description
        # 如果计费模式不常规，另外两项也不常规
        elif charge_model == 2 and (payment == '其他' or cycle == '其他'):
            dau_and_price = pay_description
        # 如果计费模式不常规，但另外两项常规
        elif charge_model == 2 and (payment != '其他' and cycle != '其他'):
            dau_and_price = pay_description + '\n' + payment_description
        # 都常规
        else:
            dau_and_price = price_description + payment_description
    return dau_and_price


async def gen_max_dau(dau_scale, charge_model, number):
    dau = ''
    if charge_model == 0:
        max_dau = 0
        for dau in dau_scale.split(' '):
            if dau:
                if len(dau.split('-')) > 1:
                    if int(dau.split('-')[1]) > max_dau:
                        max_dau = int(dau.split('-')[1])
        dau = "最高日活：{}".format(max_dau)
    elif charge_model == 1:
        dau = '-'
    else:
        sql = "select dau_max from contract_price where number=%s and is_new=1;"
        dau = 0
        result = await mysqlDB.db_select(sql, (number, ))
        if result and len(result) > 0:
            for item in result:
                if item['dau_max'] > dau:
                    dau = item['dau_max']
        dau = '最高日活{}'.format(dau)
    return dau



def decide_which_time_limit(item):
    # state=10:正在审核中,所以取time_limit;state=4:没有发生过提前终止或提前终止审核结束,time_limit先取early_time_limit后取time_limit
    if item.get('state') == 4:
        return item.get('early_time_limit') or item.get('time_limit') or 0
    else:
        return item.get('time_limit') or 0


async def get_max_groupid(number):
    groupid = 0
    sql = "select max(groupid) as groupid from contract_jointly_sign where number=%s;"
    result = await mysqlDB.db_select(sql, (number, ))
    if result and len(result) > 0:
        groupid = result[0].get('groupid') or 0
    return groupid
