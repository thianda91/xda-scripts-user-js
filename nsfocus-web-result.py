#bash
#import codecs
import os
import re
import pyperclip
from bs4 import BeautifulSoup
print("网址的扫描结果，有高危漏洞的如下：\n")
fd = open('index.html', mode='r', encoding='UTF-8')
str = fd.read()
fd.close()
soup = BeautifulSoup(str, "html.parser")
#pre_soup=soup.find_all("tbody")
#pre = pre_soup[6]
pre_soup=soup.find("div",text="2.1站点风险等级列表").parent
#pre_soup=soup.find("div",text="2.1站点风险等级列表").next_sibling.next_sibling
pre=pre_soup.tbody.find_all("tr")
result=""
for str in pre:
  if int(str.find_all("td")[3].string)>0:
    result=result+"网址\t"+str.a.string+"\t"+str.find_all("td")[3].string+"\r\n"
print(result)
pyperclip.copy(result)
print("已复制到剪切板，直接到excel粘贴即可。")
#os.system('notepad python.txt')
#import win32api
#win32api.ShellExecute(0, 'open', 'notepad.exe', 'python.txt','',1)
#win32api.ShellExecute(0, 'open', 'E:\\song.wma', '','',1)
os.system('pause')