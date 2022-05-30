import datetime
import time
import traceback

from utils import log, decorator, mysqlDB

@decorator.timer(60)
async def update_state():
    time.sleep(2)
    # try:
    #     with open('defaultGroup.txt', 'r') as f:
    #         for row in f.readlines():
    #             if not row:
    #                 continue
    #             sql = "insert into tag (name, description) values (%s, '');"
    #             args = (row.strip(),)
    #             await mysqlDB.db_exec(sql, args)
    #             print('{} ok'.format(row))
    #     # now = datetime.datetime.now()
    #     # sql = "select id, place, start_time, end_time from appointment where status=1 or status=2"
    #     # res = await mysqlDB.db_select(sql)
    #     # for item in res:
    #     #     if now > item.get('start_time'):
    #     #         to_status = 1
    #     #         if now < item.get('end_time'):
    #     #             to_status = 2
    #     #         else:
    #     #             to_status = 3
    #     #             sql = "update parking_place set status=%s where id = %s;"
    #     #             args = (2, item.get('place'))
    #     #             await mysqlDB.db_exec(sql, args)
    #     #         sql = "update appointment set status=%s where id = %s;"
    #     #         args = (to_status, item.get('id'))
    #     #         await mysqlDB.db_exec(sql, args)
    #     # sql = "select id from parking_lot;"
    #     # res = await mysqlDB.db_select(sql)
    #     # for item in res:
    #     #     sql = "select SUM(1) as total, SUM(CASE WHEN status=2 THEN 1 ELSE 0 END) as left_count from parking_place where lot_id=%s;"
    #     #     args = (item.get('id'),)
    #     #     result = await mysqlDB.db_select(sql, args)
    #     #     # log.logger.info(result)
    #     #     if result and len(result) > 0:
    #     #         sql = "update parking_lot set total_place=%s, left_place=%s where id=%s;"
    #     #         args = (result[0].get('total'), result[0].get('left_count'), item.get('id'))
    #     #         await mysqlDB.db_exec(sql, args)
    # except Exception as e:
    #     log.logger.error(e)

