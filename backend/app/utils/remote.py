import json
import asyncssh
import psutil
from utils import log, config

USERNAME = 'root'
PASSWORD = 'Guandu@903'


async def get_server_name(ip=None):
    # 获取本机IP
    try:
        if not ip:
            local_ip = ''
            info = psutil.net_if_addrs()
            for k, v in info.items():
                if k == 'en0' or k == 'eth0':
                    for item in v:
                        if item[0] == 2 and not item[1] == '127.0.0.1':
                            local_ip = item[1]
            if not local_ip:
                log.logger.error('local_ip is null.')
                return None
            ip = local_ip
        server_info = await get_server_info()
        log.logger.info('server_info = {0}.'.format(server_info))
        server_name = server_info.get(ip)
        return server_name or []
    except Exception as e:
        log.logger.error(e)
    return []


async def get_server_info():
    info = await _exec_cmd_remote(config.GATE_IP,
                                  '/home/maintain/findservers.sh')
    log.logger.info('remote : {0}'.format(info))
    obj = json.loads(info)
    server_info = {}
    for key in obj:
        if server_info.get(obj[key]) is None:
            server_info[obj[key]] = []
        server_info[obj[key]].append(key)
    return server_info


async def _exec_cmd_remote(ip, cmd, dir=None):
    if ip is None or ip == '' or cmd is None or cmd == '':
        raise Exception("param err")
    log.logger.info('connect to ip {0}'.format(ip))
    async with asyncssh.connect(
            ip, username=USERNAME, password=PASSWORD,
            known_hosts=None) as conn:
        if dir is not None:
            cmd_execute = 'cd {0}; {1}'.format(dir, cmd)
        else:
            cmd_execute = cmd
        print(cmd_execute)
        result = await conn.run(cmd_execute)

        return result.stdout
