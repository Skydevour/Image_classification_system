import asyncio
import json
# import uvloop
import sys
import traceback

import common
import httpserver
import timer
from utils import log, config, mysqlDB
import router
# from contract_debug import update_database


def get_sql_cfg(release, path):
    sql_cfg = ''
    try:
        with open(path, 'r') as f:
            sql_cfg = json.load(f)
    except Exception as e:
        log.logger.error("error info : {0}".format(e))
        log.logger.error(traceback.format_exc())
        log.logger.error("{0} error. Please check it.".format(path))
        sys.exit(1)
    if not sql_cfg:
        log.logger.error("{0} error. Please check it.".format(path))
        sys.exit(1)
    db_conf = ''
    if release:
        db_conf = sql_cfg.get('release')
    else:
        db_conf = sql_cfg.get('debug')
    if not db_conf:
        log.logger.error("{0} error. Please check it.".format(path))
        sys.exit(1)
    return db_conf


if __name__ == "__main__":
    release = 'debug'
    path = 'db.json'
    common.set_release(release)
    db_conf = get_sql_cfg(release, path)
    log.log_init(db_conf[0]['database'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mysqlDB.init(db_conf=db_conf, release=release))
    http = httpserver.init('0.0.0.0', 10051, router.add_route, loop)
    tasks = [
        http,
        mysqlDB.rebuild_db_connection_array(),
    ]
    log.logger.info("contract main started...")
    server = loop.run_until_complete(asyncio.wait(tasks))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    loop.close()
