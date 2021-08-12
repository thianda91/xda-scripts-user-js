#bash
#import codecs
import os
import re
import pyperclip
from bs4 import BeautifulSoup
print("主机IP的扫描结果，有高、中危漏洞的如下：\n")
fd = open('index.html', mode='r', encoding='UTF-8')
str = fd.read()
fd.close()
soup = BeautifulSoup(str, "html.parser")
#pre_soup=soup.find_all("div",{"id":{"title00"}})
#print(pre_soup[1])
pre_soup=soup.find_all("tr", onclick=re.compile("no_toggle\('3_1_"))
#print(pre_soup[0])
result=""
#print(pre_soup[0].find_all("td")[0].a.string)
#exit()
for str in pre_soup:
  high_vul = str.find_all("td")[3].string
  midile_vul = str.find_all("td")[4].string
  if int(high_vul)>0 or int(midile_vul)>0:
    result=result+"主机IP\t"+str.find_all("td")[0].a.string+"\t"+high_vul+"\t"+midile_vul+"\r\n"
print(result)
pyperclip.copy(result)
print("已复制到剪切板，直接到excel粘贴即可。")
#os.system('notepad python.txt')
#import win32api
#win32api.ShellExecute(0, 'open', 'notepad.exe', 'python.txt','',1)
#win32api.ShellExecute(0, 'open', 'E:\\song.wma', '','',1)
os.system('pause')