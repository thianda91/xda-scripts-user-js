#!python3

'''
screen-length 0 temporary
display interface brief main 
display interface description | exclude \.
display lldp neighbor brief
'''

'''
['Interface', 'PHY', 'Protocol', 'InUti', 'OutUti', 'inErrors', 'outErrors']
['Interface', 'PHY', 'Protocol', 'Description']
['Local Intf', 'Neighbor Dev', 'Neighbor Intf', 'Exptime (sec)']
'''

'''
取消屏幕显示长度
获取 聚合组 与 物理口 的关系、获取 物理up/down
获取 端口描述
获取 对端实际设备信息
'''


import re
from pathlib import Path
import pandas as pd
import xlsxwriter
import colorama
file_names = Path().rglob('*.log')
contents = []
for file in file_names:
    with open(file, encoding='utf-8') as f:
        contents.append(f.readlines())
        contents[-1]


def get_interfaces(content):
    '''
    获取 聚合组 端口信息、up/down、
    '''
    device_name = ''
    short_name = ''
    len_content = len(content)
    '''
    _get_device_name
    '''
    i = 0
    while True:
        r_match_name = re.search(r'<.+ME60.+>', content[i])
        if i < len_content:
            i += 1
        else:
            print('No device name was found! Abort program.')
            return
        if r_match_name != None:
            device_name = r_match_name.group(1)
            break
    # content = content[i+1:]
    flag_list = [['Interface', 'PHY', 'Protocol', 'InUti', 'OutUti', 'inErrors', 'outErrors'],
                 ['Interface', 'PHY', 'Protocol', 'Description'],
                 ['Local Intf', 'Neighbor Dev', 'Neighbor Intf', 'Exptime (sec)']]
    flag_key = ['flag_interface_brief',
                'flag_interface_desc',
                'flag_lldp_neighbor']
    while i < len_content:
        line = re.split(r' +', content[i])
        if line in flag_list:
            ...
        else:
            line += 1

    for line in content:
        s = re.split(r'  +', line)
        if s[0][:9] == 'Eth-Trunk':
            _trunk = s[0]
            continue
        if s[0] == '':
            ...

