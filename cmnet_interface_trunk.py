#!python3

'''
screen-length 0 temporary
display interface brief main
display interface description | exclude \. | ex \*down
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
file_names = Path().rglob('*.txt++')
contents = []
for file in file_names:
    with open(file, encoding='utf-8') as f:
        contents.append(f.read().splitlines())

record_list = ['Interface                   PHY   Protocol  InUti OutUti   inErrors  outErrors',
               'Interface                     PHY     Protocol Description  ',
               'Local Intf              Neighbor Dev         Neighbor Intf        Exptime (sec)'
               ]
flag_list = [['Interface', 'PHY', 'Protocol', 'InUti', 'OutUti', 'inErrors', 'outErrors'],
             ['Interface', 'PHY', 'Protocol', 'Description', ''],
             ['Local', 'Intf', 'Neighbor', 'Dev', 'Neighbor', 'Intf', 'Exptime', '(sec)']]
flag_key = ['flag_interface_brief',
            'flag_interface_desc',
            'flag_lldp_neighbor']


def get_device_name(content=[]) -> str:
    '''
    获取设备名
    '''
    device_name = ''
    len_content = len(content)
    i = 0
    while True:
        r_match_name = re.search(r'<(.+ME60.+)>', content[i])
        if r_match_name != None:
            device_name = r_match_name.group(1)
            break
        if i < len_content:
            i += 1
        else:
            print('No device name was found! Abort program.')
            return
    return device_name


def get_device_nick_name(device_name='') -> str:
    '''
    获取设备别名
    '''
    return re.search(r'BAS[0-9]+', device_name).group(0)


def get_start_index(content=[], flag=[]) -> int:
    '''
    定位数据采集起始点
    '''
    for index, value in enumerate(content):
        _list = re.split(r' +', value)
        if _list == flag:
            return index + 1
    return False


def get_interfaces(content=[]) -> list:
    '''
    获取 聚合组 端口信息、up/down、
    当前匹配 ME60
    '''
    # 定位数据采集起始点
    _start = get_start_index(content, flag_list[0])
    if not _start:
        print('无法定位数据采集点', 'get_interfaces')
        return []
    device_name = get_device_name(content)
    interfaces = []
    for value in content[_start:]:
        # 定位数据采集结束点
        if device_name in value:
            break
        _list = re.split(r' +', value)
        if _list[0][:9] == 'Eth-Trunk':
            _trunk = _list[0]
            phy = '{}-{}'.format(_list[1], _list[2])
            interfaces.append([device_name, '-', '-', _trunk, _trunk, phy])
        elif _list[0] == '':
            port = _list[1]
            r = re.search(r'([0-9]+)/([0-9]+)/', port)
            frame = r.group(1)
            solt = r.group(2)
            phy = '{}-{}'.format(_list[2], _list[3])
            interfaces.append([device_name, frame, solt, port, _trunk, phy])
        elif 'LoopBack' in _list[0] or 'NULL' in _list[0] or 'irtual' in _list[0]:
            continue
        else:
            port = _list[0]
            r = re.search(r'([0-9]+)/([0-9]+)/', port)
            frame = r.group(1)
            solt = r.group(2)
            phy = '{}-{}'.format(_list[1], _list[2])
            interfaces.append([device_name, frame, solt, port, '-', phy])

    return interfaces


def get_desc(content=[]) -> list:
    '''
    获取端口描述
    '''
    # 定位数据采集起始点
    _start = get_start_index(content, flag_list[1])
    if not _start:
        print('无法定位数据采集点', 'get_desc')
        return []
    device_name = get_device_name(content)
    desc = []
    for value in content[_start:]:
        # 定位数据采集结束点
        r = re.search(device_name, value)
        if r and r.start() < 3:
            break
        _list = re.split(r' +', value)
        port = _list[0]
        if 'GE' in port:
            port = port.replace('GE', 'GigabitEthernet')
        elif not 'Eth-Trunk' in port:
            break
        description = _list[3]
        desc.append([port, description])

    return desc


def get_lldp(content=[])-> list:
    '''
    获取 lldp 信息
    '''
    # 定位数据采集起始点
    _start = get_start_index(content, flag_list[2])
    if not _start:
        print('无法定位数据采集点', 'get_interfaces')
        return []
    device_name = get_device_name(content)
    interfaces = []
    for value in content[_start:]:
        # 定位数据采集结束点
        if device_name in value:
            break
        _list = re.split(r' +', value)
        ...





for content in contents:
    ...
    # interfaces = get_interfaces(content)
    # print(interfaces)
    # desc = get_desc(content)
    # print(desc)
    
