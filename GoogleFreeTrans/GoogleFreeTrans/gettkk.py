# -*- coding:utf-8 -*-
import requests
import re
import execjs
import time


def get_res(url):
    """get raw html from 'https://translate.google.cn/' """
    time_interval = 3
    try:
        time.sleep(time_interval)
        result = requests.get(url, timeout = 1.5)
        result.raise_for_status()
        #result.encoding = 'utf-8'
    except Exception as ex:
        print('function get_res [-]ERROR: ' + str(ex))
        result = requests.models.Response#返回一个空的结果
        print(result.text)

    return result


def get_tkk():
    """get the tkk"""
    url = 'https://translate.google.cn/'
    retry = 3
    time_interval = 3
    while retry > 0:
        try:
            res = get_res(url)

            tkk = re.search(r'tkk\:\'(\d+\.\d+)?\'', res.text).group(1)
            return tkk
        except Exception as ex:
            print('function get_tkk [-]ERROR: ' + str(ex))
            time.sleep(time_interval)
            time_interval += 1
            retry -= 1

    return 0.0
