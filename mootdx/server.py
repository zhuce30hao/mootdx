# -*- coding: utf-8 -*-
import logging
import socket
import time

from mootdx.consts import EX_HOSTS, GP_HOSTS, HQ_HOSTS
from prettytable import PrettyTable

logger = logging.getLogger(__name__)
result = []

hosts = {
    'HQ': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in HQ_HOSTS],
    'EX': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in EX_HOSTS],
    'GP': [{'addr': hs[1], 'port': hs[2], 'time': 0, 'site': hs[0]} for hs in GP_HOSTS],
}


def Server(index=None, limit=5, console=False, verbose=False):
    if verbose:
        logging.basicConfig(level='DEBUG')

    _hosts = hosts[index]
    server = []

    while True:
        if len(_hosts) == 0:
            break

        try:
            proxy = _hosts.pop()
        except ValueError:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        try:
            start = time.clock()

            sock.connect((proxy.get('addr'), int(proxy.get('port'))))
            sock.close()

            proxy['time'] = (time.clock() - start) * 1000

            server.append(proxy)
            logger.info("{}:{} 验证通过，响应时间：{:.2} ms.".format(proxy.get('addr'), proxy.get('port'), proxy.get('time')))
        except Exception:
            logger.warning("{},{} 验证失败.".format(proxy.get('addr'), proxy.get('port')))

    # 结果按响应时间从小到大排序
    server.sort(key=lambda item: item['time'])

    if console:
        print("[√] 最优服务器:")

        t = PrettyTable(["Name", "Addr", "Port", "Time"])
        t.align["Name"] = "l"
        t.align["Addr"] = "l"
        t.align["Port"] = "l"
        t.align["Time"] = "r"
        t.padding_width = 1

        for host in server[:int(limit)]:
            t.add_row([host['site'], host['addr'], host['port'], '{:.2} ms'.format(host['time'])])

        print(t)

    return [(item['addr'], item['port']) for item in server]
