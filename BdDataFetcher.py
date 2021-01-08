#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import logging
import time

import requests
import re
import json

class BdDataFetcher(object):
    def __init__(self):
        self.url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
        self.request_session = requests.session()
        self.request_session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }

    def request(self, year_month):
        payload = {
            'query': year_month,
            'resource_id': 39043,
            't': int(round(time.time() * 1000)),
            'ie': 'utf8',
            'oe': 'utf8',
            'cb': 'op_aladdin_callback',
            'format': 'json',
            'tn': 'wisetpl',
            'cb': 'jQuery110206747607329442493_1606743811595',
            '_': 1606743811613
        }
        resp = self.request_session.get(url=self.url, params=payload)
        logging.debug('data fetcher resp = {}'.format(resp.text))
        bracket_pattern = re.compile(r'[(](.*?)[)]', re.S)
        valid_data = re.findall(bracket_pattern, resp.text)
        json_data = json.loads(valid_data[0])
        almanac = json_data['data'][0]['almanac']
        result = {}
        for day in almanac:
            key = '{}-{}-{}'.format(day['year'], day['month'],day['day'])
            result[key] = day
        return result
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    BdDataFetcher().request('2021年1月')
