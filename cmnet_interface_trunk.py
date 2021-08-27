#!python3

'''
screen-length 0 temporary
display interface brief main
display interface description | exclude \.
display lldp neighbor
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


# init(autoreset=True)
import re
from pathlib import Path
import pandas as pd
from colorama import Fore, Back, Style, init
import platform
init(autoreset=True)
if platform.system() == 'Windows':
    init(wrap=True)
file_names = Path().rglob('*.log')
contents = []
for file in file_names:
    if file == 'AutoRun.log':
        continue
    try:
        with open(file, encoding='utf-8') as f:
            contents.append(f.read().splitlines())
    except:
        ...

record_list = ['Interface                   PHY   Protocol  InUti OutUti   inErrors  outErrors',
               'Interface                     PHY     Protocol Description  ',
               'Local Intf              Neighbor Dev         Neighbor Intf        Exptime (sec)'
               ]
flag_list = [['Interface', 'PHY', 'Protocol', 'InUti', 'OutUti', 'inErrors', 'outErrors'],
             ['Interface', 'PHY', 'Protocol', 'Description', ''],
             ['Local', 'Intf', 'Neighbor', 'Dev', 'Neighbor', 'Intf', 'Exptime', '(sec)']]
flag_list = [['Interface', 'PHY', 'Protocol', 'InUti'],
             ['Interface', 'PHY', 'Protocol', 'Description'],
             ['Local', 'Intf', 'Neighbor', 'Dev']]
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
        r_match_name = re.search(r'<(.+[ME60|CMNET\-SW].+)>', content[i])
        if r_match_name != None:
            device_name = r_match_name.group(1)
            return device_name
        elif i < len_content:
            i += 1
        else:
            print('No device name was found! Abort program.')
            return ''


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
        if _list[:4] == flag:
            return index + 1
    return False


def get_interfaces(content=[]) -> list:
    '''
    获取 聚合组 端口信息、up/down、
    当前匹配 ME60
    '''

    def _get_frame_slot(port):
        r = re.search(r'([0-9]+)/([0-9]+)', port)
        frame = r.group(1)
        solt = r.group(2)
        return frame, solt

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
            frame, solt = _get_frame_slot(port)
            phy = '{}-{}'.format(_list[2], _list[3])
            interfaces.append([device_name, frame, solt, port, _trunk, phy])
        elif 'Ethernet' in _list[0]:
            port = _list[0]
            frame, solt = _get_frame_slot(port)
            phy = '{}-{}'.format(_list[1], _list[2])
            interfaces.append([device_name, frame, solt, port, '-', phy])
        else:
            continue

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
            if '100GE' not in port:
                port = port.replace('GE', 'GigabitEthernet')
        elif not 'Eth-Trunk' in port:
            continue
        description = ''.join(_list[3:])
        # print(device_name, 'port', Fore.GREEN+port)
        # print('description', Fore.GREEN+description)
        desc.append([port, description])
    return desc


def get_lldp(content=[]) -> list:
    '''
    获取 lldp 信息
    '''
    # 定位数据采集起始点
    # _start = get_start_index(content, flag_list[2])
    _start = False
    for index, value in enumerate(content):
        _list = re.split(r' +', value)
        if len(_list) == 4 and _list[1] == 'has' and _list[3][:8] == 'neighbor':
            _start = index
            break
    if not _start:
        print('无法定位数据采集点', 'get_lldp')
        return []
    device_name = get_device_name(content)
    lldp = []
    for value in content[_start:]:
        # 定位数据采集结束点
        # if re.search(r'[<\[][~\*]?'+device_name+'.+', value):
        #     break
        r = re.search(device_name, value)
        if r and r.start() < 3:
            break
        _list = re.split(r' +', value)
        # lldp.append([_list[0], _list[1], _list[2]])
        if len(_list) == 4 and _list[1] == 'has' and _list[3][:8] == 'neighbor':
            port2 = _list[0]
            # print('port2',Back.BLUE+port2)
        elif value[:9] == 'Port ID  ':
            lldp_port = _list[2][1:]
            # print('Port ID',Fore.GREEN+lldp_port)
        elif value[:13] == 'System name  ':
            lldp_device = _list[2][1:]
            # print('System name',Fore.GREEN+lldp_device)
        elif value[:20] == 'System description  ':
            lldp_desc = ''.join(_list[2:])[1:]
            # print('System description',Fore.GREEN+lldp_desc)
            lldp.append([port2, lldp_device, lldp_desc, lldp_port])
        elif _list[0] == 'PortId:':
            lldp_port = _list[1]
            # print('PortId:',Fore.BLUE+lldp_port)
        elif _list[0] == 'SysName:':
            lldp_device = _list[1]
            # print('SysName',Fore.BLUE+lldp_device)
        elif _list[0] == 'SysDesc:':
            lldp_desc = ''.join(_list[1:])
            # print('SysDesc',Fore.BLUE+lldp_desc)
            lldp.append([port2, lldp_device, lldp_desc, lldp_port])
    return lldp


datas = pd.DataFrame()
for content in contents:
    # try:
    interfaces = get_interfaces(content)
    # print(interfaces)
    desc = get_desc(content)
    # print(desc)
    lldp = get_lldp(content)
    # print(lldp)
    df_interface = pd.DataFrame(
        interfaces, columns=['device', 'frame', 'slot', 'port', 'trunk', 'status'])
    df_desc = pd.DataFrame(desc, columns=['port', 'description'])
    df_lldp = pd.DataFrame(
        lldp, columns=['port2', 'lldp_device', 'lldp_desc', 'lldp_port'])
    data = df_interface.merge(df_desc, how='left', on='port').fillna('')
    data['port2'] = data['port'].map(
        lambda port: port.replace('(10G)', '').replace('(100G)', ''))
    data = data.merge(df_lldp, how='left', on='port2').fillna('')
    data.drop('port2', axis=1, inplace=True)
    datas = datas.append(data, ignore_index=True)
    # except Exception as err:
    #     print(Back.RED+str(err))

datas.sort_values(by=['device', 'frame', 'slot'], inplace=True)
try:
    writer = pd.ExcelWriter('output.xlsx')
    datas.to_excel(writer, index=False)
    writer.save()
except Exception as err:
    print(Back.RED+str(err))
