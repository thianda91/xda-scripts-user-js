#!python3

# UserClick('%e7%94%b5%e5%ad%90%e8%bf%90%e8%a1%8c..','%2f_layouts%2fDocument%2fBridgeToSPControl.aspx%3fskipcode%3demoss')

# # EOMS：
# http://uip.ln.cmcc/_layouts/Document/BridgeToSPControl.aspx?skipcode=emoss

# http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action
# ?id=402894f5295e64ce01295e71d01e0001

# # 故障处理工单(设备)：
# http://10.204.14.35/eoms4/sheetBpp/myWaitingDealSheetQueryGlobalTemplate.action?baseSchema=WF4_EL_TTM_TTH_EQU
# &id=8a4c8e9f605487a9016057a5d21f016e


# from bs4 import BeautifulSoup as bs

from xdaLibs import iniconfig
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.ie.options import Options
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from threading import Timer
from datetime import datetime
import re
import os
import sys
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

configFile = 'dist/config.work.ini'
conf = iniconfig.IniConfig(configFile, encoding='gbk')
username = conf.get('UIP', 'u')
password = conf.get('UIP', 'p')
exe = conf.get('common', 'exe')
if '' == conf.get('UIP', 'proxies'):
    proxies = None
else:
    proxies = {"http": conf.get('UIP', 'proxies')}

print('proxies:', proxies)


def datef(x=None):
    if x == None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return x.strftime("%Y-%m-%d %H:%M:%S")


def datep(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')


def getBrowser(exe):
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Ie(executable_path=exe)
    # browser = webdriver.Chrome(executable_path=exe)
    return browser


def autoLogin(browser: WebDriver) -> WebDriver:
    uip_url = 'http://uip.ln.cmcc/'
    browser.get(uip_url)
    browser.find_element(By.ID, 'UserName').clear()
    browser.find_element(By.ID, 'UserName').send_keys(username)
    browser.find_element(By.ID, 'password').clear()
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.ID, 'login').click()
    if 'Login' in browser.current_url:
        pauseAndExit('登录未成功，请检查配置文件中的账号密码是否正确。并重新运行！')

    def loopRefresh(inc, window_handle, url):
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        browser.switch_to.window(window_handle)
        browser.get(url)
        t = Timer(inc, loopRefresh, (inc, window_handle, url,))
        t.start()
        # 10min
    loopRefresh(600, browser.window_handles[0], uip_url)
    return browser


def jumpToEOMS(browser: WebDriver) -> WebDriver:
    eoms_url = 'http://uip.ln.cmcc/_layouts/Document/BridgeToSPControl.aspx?skipcode=emoss'
    browser.get(eoms_url)
    loginName = re.search('loginName=(.+)', browser.current_url)
    if loginName == None:
        exit()
    else:
        loginName = loginName.group(1)
    eoms_new = 'http://10.204.137.51/api/auth/oauth/token?grant_type=sso&client_id=uip&client_secret=uip&token={}'
    eoms_old = 'http://eoms.nmc.ln.cmcc/eoms4/portal/uiplogin.action?source=uip&loginName={}'
    browser.get(eoms_old.format(loginName))
    return browser


def getOrders(browser: WebDriver, orderType='') -> list:
    # 故障处理工单(设备)：
    if orderType == '[数据网]':
        todo_list_url = 'http://10.204.14.35/eoms4/sheetBpp/myWaitingDealSheetQueryGlobalTemplate.action?baseSchema=WF4_EL_TTM_TTH_EQU&id=8a4c8e9f605487a9016057a5d21f016e&var_pagesize=100'
        # todo_list_url = 'http://10.204.137.51/eoms/wait/?baseSchema=WF4_EL_TTM_TTH_EQU#/'
    elif orderType == '[通知]':
        todo_list_url = 'http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action?baseSchema=WF4_EL_TTM_TTH_NOTICE&id=8a4c8ea376938d3d0176944e21980ab4&var_pagesize=100'
    elif orderType == '[平台]':
        todo_list_url = 'http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action?baseSchema=WF4_EL_TTM_TTH_PLAT&id=8a4c8ea36d4783fb016d4855a49b088e&var_pagesize=100'
    browser.get(todo_list_url)
    total_ele = 'form#form1 span.pagenumber'
    total_element = browser.find_element(By.CSS_SELECTOR, total_ele)
    total = re.search(r'共([0-9]+)条数据', total_element.text).group(1)
    # oo = $('table#tab tr')
    # Array.prototype.shift.apply(oo)
    todo_list = browser.find_elements(
        By.CSS_SELECTOR, 'table#tab tr')[1:]

    def get_url(title_ele):
        onclick = title_ele.find_element_by_tag_name(
            'a').get_attribute('onclick')
        args = re.findall(r'\'(.*?)\'', onclick)
        # browser.execute_script('')
        url = 'http://10.204.14.35/eoms4/sheet/openWaittingSheet.action?baseSchema={}&taskid={}&baseId={}&entryId=&version=&processType={}'
        url = url.format(args[0], args[2], args[1], args[3])
        # url = 'http://10.204.14.31:8001/bpp/ultrabpp/view.action?baseSchema={}&baseId={}&taskid={}&processType={}'
        # url = url.format(args[0], args[1], args[2], args[3])
        return url

    data = []
    # 待处理工单统计
    i = 0
    for x in range(0, int(total)):
        title = todo_list[2*x+1]
        if title.text.find(orderType) != -1:
            data.append({})
            data[i]['title'] = title.text[21:]
            content = todo_list[2*x].find_elements_by_tag_name('td')
            data[i]['end_time'] = datep(content[4].text)
            data[i]['find_time'] = datep(content[5].text)
            data[i]['status'] = content[6].text
            data[i]['url'] = get_url(title)
            i += 1
    return data


def getOrderDetails(browser: WebDriver, data: list, orderType='') -> list:
    # 上清除时间的工单统计
    data2 = []
    # 未上清除时间统计
    data3 = []
    j = 0
    for x in range(len(data)):
        # 访问每一条工单
        browser.get(data[x]['url'])
        data[x]['clear_time'] = browser.find_element_by_id(
            'INC_Alarm_ClearTime').get_attribute('value')
        data[x]['happen_time'] = browser.find_element_by_id(
            'INC_HappenTime').get_attribute('value')
        data[x]['found_time'] = browser.find_element_by_id(
            'INC_FoundTime').get_attribute('value')
        title_match = re.search(r'([A-Z\-0-9]+) 上报 (.+)', data[x]['title'])
        try:
            data[x]['device'] = title_match.group(1)
            data[x]['event'] = title_match.group(2)
        except:
            pass
        if data[x]['clear_time'] != '':
            data2.append(data[x])
            j += 1
        else:
            data3.append(data[x])

    # TODO 详细推送
    msg_title = '{}故障工单 {} 个，已上清除 {} 个。'
    msg_title = msg_title.format(orderType, len(data), len(data2))
    find_time2, find_time3 = [], []
    if data2 != []:
        for x in data2:
            find_time2.append('{}, {}'.format(
                x['happen_time'], datef(x['find_time'])[-8:]))
    if data3 != []:
        for x in data3:
            find_time3.append('{}, {}'.format(
                x['happen_time'], datef(x['find_time'])[-8:]))
    msg_text = '### {}\n\n> 推送时间：{}\n\n故障发生时间&建单时间如下\n\n**已上清除**：\n\n{}\n\n**未上清除**：\n\n{}'
    t2, t3 = '\n\n'.join(find_time2), '\n\n'.join(find_time3)
    msg_text = msg_text.format(msg_title, datef(), t2, t3)
    send_msg(msg_markdown(msg_title, msg_text, True))

    jumpToEOMS(browser)
    return data, data2, data3


def jumpToLevel3(browser: WebDriver):
    # 故障管理工单(通知)
    url = 'http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action?baseSchema=WF4_EL_TTM_TTH_NOTICE&id=8a4c8ea376938d3d0176944e21980ab4'
    browser.get(url)

    def get_url(title_ele):
        onclick = title_ele.find_element_by_tag_name(
            'a').get_attribute('onclick')
        args = re.findall(r'\'(.*?)\'', onclick)
        # browser.execute_script('')
        url = 'http://10.204.14.35/eoms4/sheet/openWaittingSheet.action?baseSchema={}&taskid={}&baseId={}&entryId=&version=&processType={}'
        url = url.format(args[0], args[2], args[1], args[3])
        # url = 'http://10.204.14.31:8001/bpp/ultrabpp/view.action?baseSchema={}&baseId={}&taskid={}&processType={}'
        # url = url.format(args[0], args[1], args[2], args[3])
        return url
    ...

    '''
    #  故障管理工单(平台) (MDCN)
    http://10.204.14.35/eoms4/sheet/myWaitingDealSheetQuery.action?baseSchema=WF4_EL_TTM_TTH_PLAT&id=8a4c8ea36d4783fb016d4855a49b088e

    '''


def batchAccept(browser: WebDriver):
    # 批量受理
    u = 'http://10.204.14.35/eoms4/sheetBpp/myWaitingDealSheetQueryty.action?baseSchema=WF4_EL_TTM_TTH_EQU&var_pagesize=100'
    browser.get(u)
    total_ele = 'form#form1 span.pagenumber'
    total_element = browser.find_element(By.CSS_SELECTOR, total_ele)
    total = re.search(r'共([0-9]+)条数据', total_element.text).group(1)
    if total < 1:
        return
    todo_list = browser.find_elements(
        By.CSS_SELECTOR, 'table#tab tr')[1:]
    data = []
    i = 0
    for x in range(0, int(total)):
        title = todo_list[2*x+1].text
        if title.find('[数据网]') != -1:
            checkbox = todo_list[2*x].find_element(By.NAME, 'checkid')
            checkbox.click()

    # batchAccept_btn = browser.find_element(By.CSS_SELECTOR, 'li.page_active_button')
    browser.execute_script('batchAccept();')


def pauseAndExit(text=''):
    print(text)
    os.system('pause')
    sys.exit()


def url_with_sign():
    hook_url = 'https://oapi.dingtalk.com/robot/send?access_token=fe2ef3306c967ca646fc58d9c33a347e1a7dcd45d27a857670c7a912bb5cb14b'
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC49aeb77b3c0d15e9e6953d2bb9619c784efd08ec53d091682af3de6fc45e3615'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    signStr = '{}&timestamp={}&sign={}'.format(hook_url, timestamp, sign)
    return signStr


def send_msg(msg):
    header = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.post(
        url_with_sign(), headers=header, data=msg, proxies=proxies)
    if response.status_code != 200:
        print('推送异常！')
        print(json.loads(response.text))
    # print(response.status_code)


def msg_text(text: str, isAtAll: bool = False, atMobiles: str = ''):
    data = {'msgtype': 'text', 'text': {'content': ''},
            'at': {'atMobiles': [], 'isAtAll': False}}
    data['text']['content'] = text
    data['at']['isAtAll'] = isAtAll
    if not isAtAll:
        if isinstance(atMobiles, str):
            data['at']['atMobiles'] = [atMobiles]
        if isinstance(atMobiles, list):
            data['at']['atMobiles'] = atMobiles
    # return data
    # json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=0)
    json_str = json.dumps(data)
    # json_str.replace(' ', '')
    return json_str


def msg_markdown(title: str, text: str, isAtAll: bool = False, atMobiles: str = ''):
    data = {'msgtype': 'markdown', 'markdown': {'title': '', 'text': ''},
            'at': {'atMobiles': [], 'isAtAll': False}}
    data['markdown']['title'] = title
    data['markdown']['text'] = text
    data['at']['isAtAll'] = isAtAll
    if not isAtAll:
        if isinstance(atMobiles, str):
            data['at']['atMobiles'] = [atMobiles]
        if isinstance(atMobiles, list):
            data['at']['atMobiles'] = atMobiles
    json_str = json.dumps(data)
    # json_str.replace(' ', '')
    return json_str


if __name__ == "__main__":
    ...

    def loop(inc):
        # try:
        browser = getBrowser(exe)
        autoLogin(browser)
        jumpToEOMS(browser)
        data = getOrders(browser, '[数据网]')
        getOrderDetails(browser, data, '[数据网]')
        browser.switch_to.default_content()
        browser.quit()
        # except Exception as err:
        #     ...
        #     print(err)
        #     browser.quit()
        print('* 当前时间：', datef())
        t = Timer(inc, loop, (inc,))
        t.start()
    loop(3600)
    # exit()
