# coding:utf-8
import json
import os
import random


def random_ua():
    path = os.path.abspath(os.path.dirname(__file__) + '/data/useragent.json')
    uas = json.loads(open(path).read())
    ua = random.choice(uas[random.choice(list(uas.keys()))])
    return ua


def random_header():
    return {
        'User-Agent': random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Cache-Control': 'max-age=0'
    }


def random_proxy():
    # p = os.path.abspath(os.path.dirname(__file__) + './data/proxies.json')
    # proxy = json.loads(open(p).read())
    # proxy = random.choice(data[random.choice(list(data.keys()))])
    port = random.randint(8081, 8082)
    proxy = {'http': 'socks5://127.0.0.1:%d' % port,
             'https': 'socks5://127.0.0.1:%d' % port}
    return proxy
