#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import re

__version__ = 'v2020.09.14'


def query(result_filter):
    with open(file_name, 'r') as f:
        ip_string = f.read()
        ip_array = ip_string.splitlines()

    print('已识别到 ip 地址 {} 个，正在查询归属...'.format(len(ip_array)))
    ans = []
    for i in ip_array:
        res = result_filter(i)
        ans.append(res)
        time.sleep(0.01)

    out_str = '\n'.join(ans)

    with open(out_file, 'w') as f:
        f.write(out_str)

    print('查询结束，结果在当前目录下的 {} 中。'.format(out_file))
    end = time.time()
    print('运行耗时： {:.2f} 秒'.format(end-start))


def get_ip_pconline(ip):
    url_pconline = 'http://whois.pconline.com.cn/ip.jsp'
    res = requests.get('{}?ip={}'.format(url_pconline, ip), headers=header)
    return res.text.strip()


def get_ip_chinaz(ip):
    url_chinaz = 'http://ip.tool.chinaz.com/ajaxsync.aspx?at=ipbatch'
    res = requests.get('{}&ip={}'.format(url_chinaz, ip), headers=header)
    ans = re.search('location:\'(.+)\'', res.text)
    if ans:
        return ans.group(1)
    else:
        return "未知"


if __name__ == '__main__':
    file_name = 'ip.txt'
    out_file = 'output.txt'
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }
    print('\n\t**********************************************')
    print('\tip 地址归属查询小工具 {}'.format(__version__))
    print('\t**********************************************')
    print('\t\t作者：X.Da\n\n')
    start = time.time()
    try:
        # query(get_ip_chinaz)
        query(get_ip_pconline)
    except Exception as e:
        print('出错了：{}'.format(e))
        print('\n\n\t请阅读使用帮助： ip_locate.readme.txt\n\n')

    print('***按回车退出...')
    input()
