import asyncio
import aiohttp
import time
import sys
import re

import requests

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=ALLOW_REDIRECTS, headers=DEFAULT_HEADERS) as response:
                    if response.status in VALID_STATUS_CODES:
                        print('代理可用', proxy)
                        self.redis.max(proxy)
                    else:
                        print('请求响应码不合法 ', response.status, 'IP', proxy)
                        self.redis.decrease(proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    async def test_pddsearch_proxy(self, proxy):
        """
        测试拼多多搜索代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=ALLOW_REDIRECTS, headers=DEFAULT_HEADERS) as response:
                    result = await response.text()
                    list_id = re.findall('"list_id.*?".*?"(.*?)"', result, re.S)
                    if response.status in VALID_STATUS_CODES and list_id:
                        print('代理可用', proxy)
                        self.redis.max(proxy)
                    else:
                        print('请求响应码不合法 ', response.status, 'IP', proxy)
                        self.redis.decrease(proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                a = 'self.{method}'.format(method=TEST_METHOD)
                tasks = [self.test_pddsearch_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
