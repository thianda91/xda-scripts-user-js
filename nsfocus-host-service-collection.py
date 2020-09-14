#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
import pyperclip


def collect(f, td):
    """采集当前 tr 内的 info"""
    line = []
    ip = f[:-5]
    port = td[0].string
    service = td[2].string
    danger_high = td[3].select('span.level_danger_high')
    marks = ''
    if danger_high == []:
        danger_high_len = '0'
    else:
        danger_high_len = str(len(danger_high))
        # marks 取固定值，为漏洞详细信息截取空格前的字符串。
        marks = danger_high[0].string.split(' ')[0]
    danger_middle = td[3].select('span.level_danger_middle')
    if danger_middle == []:
        danger_middle_len = '0'
    else:
        danger_middle_len = str(len(danger_middle))
    line = [ip, port, service, danger_high_len, danger_middle_len, marks]
    return line


def removeDup(_list):
    new_list = []
    for i in _list:
        if i not in new_list:
            new_list.append(i)
    return new_list


def getInfo(td):
    """获取漏洞详细信息"""
    tr = [t.find_parent('tr') for t in td]
    tr = removeDup(tr)
    port = ';'.join([t.find_all('td')[0].string for t in tr])
    service = ';'.join([t.find_all('td')[2].string for t in tr])
    marks = [t.string.split(' ')[0] for t in td]
    marks = removeDup(marks)
    marks = ';'.join(marks)
    return port, service, marks


def main():
    forder = 'host' + os.sep
    filenames = [i for i in os.listdir(forder) if '.html' in i]
    result = [['ip', '高危', '中危', 'port', 'service', 'marks']]
    for f in filenames:
        no_danger = True
        fd = open(forder + f, mode='r', encoding='UTF-8')
        html = fd.read()
        fd.close()
        soup = BeautifulSoup(html, "html.parser")
        vuln_list = soup.select("#vuln_list tr")
        if vuln_list == []:
            continue
        vuln_list.pop(0)  # 去除 title
        danger_high = soup.select('#vuln_list tr td span.level_danger_high')
        danger_middle = soup.select(
            '#vuln_list tr td span.level_danger_middle')
        if danger_high == []:
            danger_high_len = '0'
        else:
            danger_high_len = str(len(danger_high))
            no_danger = False
            port, service, marks = getInfo(danger_high)
        if danger_middle == []:
            danger_middle_len = '0'
        else:
            danger_middle_len = str(len(danger_middle))
            no_danger = False
            if 'port' not in locals():
                port, service, marks = getInfo(danger_middle)
        if no_danger:
            continue
        else:
            ip = f[:-5]
            result.append(
                [ip, danger_high_len, danger_middle_len, port, service, marks])
    r = []
    for x in result:
        r.append('\t'.join(x))
    result = '\n'.join(r)
    pyperclip.copy(result)
    print(result[0])
    # os.system('notepad python.txt')
    # import win32api
    # win32api.ShellExecute(0, 'open', 'notepad.exe', 'python.txt','',1)
    # win32api.ShellExecute(0, 'open', 'E:\\song.wma', '','',1)
    os.system('pause')


if __name__ == '__main__':
    main()
