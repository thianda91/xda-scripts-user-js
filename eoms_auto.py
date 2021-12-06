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
# from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.ie.options import Options
from selenium.webdriver.chrome.options import Options
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
import urllib.request
import requests

configFile = 'dist/config.work.ini'
conf = iniconfig.IniConfig(configFile, encoding='gbk')
username = conf.get('UIP', 'u')
password = conf.get('UIP', 'p')
exe = conf.get('common', 'exe_chrome')
if '' == conf.get('UIP', 'proxies'):
    proxies = None
else:
    proxies = {"http": conf.get('UIP', 'proxies')}
    print('proxies:', proxies)

args = sys.argv[1:]


def datef(x=None):
    if x == None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return x.strftime("%Y-%m-%d %H:%M:%S")


def datep(x): return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')


def try_func(func, showErr=False) -> int:
    ret = 0
    try:
        ret = func()
    except Exception as err:
        if showErr:
            print(err)
    return ret


def getBrowser(exe, browser_type='chrome'):
    options = Options()
    if '-w' in args:
        options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('blink-settings=imagesEnabled=false')
    if browser_type == 'ie':
        return webdriver.Ie(executable_path=exe)
    if browser_type == 'chrome':
        return webdriver.Chrome(options=options, executable_path=exe)


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
        try:
            browser.switch_to.window(window_handle)
            browser.get(url)
            browser.back()
            t = Timer(inc, loopRefresh, (inc, window_handle, url,))
            t.start()
        except Exception as err:
            print('********autoLogin-loopRefresh-ERR********')
            print(err)
        # 10min
    loopRefresh(650, browser.window_handles[0], uip_url)
    return browser


def jumpToEOMS(browser: WebDriver, version='new') -> WebDriver:
    eoms_url = 'http://uip.ln.cmcc/_layouts/Document/BridgeToSPControl.aspx?skipcode=emoss'
    browser.get(eoms_url)
    # loginName = re.search('loginName=(.+)', browser.current_url)
    # if loginName == None:
    #     exit()
    # else:
    #     loginName = loginName.group(1)

    # eoms_url = 'http://10.204.137.51/api/auth/oauth/token?grant_type=sso&client_id=uip&client_secret=uip&token={}'
    # if version == 'old':
    #     eoms_url = 'http://eoms.nmc.ln.cmcc/eoms4/portal/uiplogin.action?source=uip&loginName={}'

    # browser.get(eoms_url.format(loginName))
    browser.find_element(By.CSS_SELECTOR, 'div.{}eoms'.format(version)).click()
    wait = WebDriverWait(browser, 5)
    _selector = 'span.username' if version == 'new' else '#timeBox'
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, _selector)))
    # browser.get('http://10.204.137.51/eoms/')
    return browser


def getOrdersNew(browser: WebDriver, orderType='') -> list:
    '''
    获取推送信息 新版eoms
    '''
    baseSchema = {'[数据网]': 'WF4_EL_TTM_TTH_EQU',
                  '[通知]': 'WF4_EL_TTM_TTH_NOTICE'}
    todo_list_url = 'http://10.204.137.51/eoms/wait/?baseSchema={}#/'.format(
        baseSchema[orderType])
    browser.get(todo_list_url)
    total_element = browser.find_element(
        By.CSS_SELECTOR, '.ant-pagination-total-text')
    total = re.search(r'[0-9]+', total_element.text).group()
    todo_list = browser.find_elements(
        By.CSS_SELECTOR, 'table#tab tr')[1:]

    # query_url = 'http://10.204.137.51/api/query/query/querylist'
    # payload = {
    #     "id": "wait",
    #     "params": {
    #         "basesummary": "[数据网]", "isfull": "1", "baseschema": "WF4_EL_TTM_TTH_EQU"
    #     },
    #     "sorter": {},
    #     "pageNum": 1,
    #     "pageSize": 200
    # }
    # jq = 'http://uip.ln.cmcc/_layouts/15/styles/css_4nd/js/jquery1.42.min.js'
    # jq = 'http://10.204.137.51/bpp/common/plugin/jquery/jquery-1.9.1.min.js'
    # jquery_str = urllib.request.urlopen(jq).read().decode()
    # browser.execute_script(jquery_str)
    # ajax_query = '''
    # $.post({},{{data:{}}})
    # '''.format(query_url, payload)
    # resp = browser.execute_script("return " + ajax_query)

    # post_data = urllib.parse.urlencode(payload).encode('utf-8')
    # req = urllib.request.Request(url=query_url, headers=headers, data=post_data, method='POST')
    # response = urllib.request.urlopen(req)
    # html = response.read().decode()
    # data = json.loads(html)


def getOrders(browser: WebDriver, orderType='') -> list:
    '''
    获取推送信息 旧
    '''
    jumpToEOMS(browser, 'old')
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
        onclick = title_ele.find_element(
            By.TAG_NAME, 'a').get_attribute('onclick')
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
            content = todo_list[2*x].find_elements(By.TAG_NAME, 'td')
            data[i]['end_time'] = datep(content[4].text)
            data[i]['find_time'] = datep(content[5].text)
            data[i]['status'] = content[6].text
            data[i]['url'] = get_url(title)
            i += 1
    return data


def getOrderDetails(browser: WebDriver) -> list:
    alarm_desc = browser.find_element(By.ID, 'INC_Alarm_Desc').text

    def _find(_reg, _txt):
        try:
            result = re.search(_reg, _txt).group(1)
        except:
            result = ''
        return result

    alarm_title = _find(r'告警名称：(.+)', alarm_desc)
    # alarm_dev = _find(r'告警网元：(.+)', alarm_desc)
    # alarm_ip = _find(r'网元IP：(.+)', alarm_desc)
    alarm_time = _find(r'告警时间：(.+)', alarm_desc)
    # alarm_port1 = _find(r'Trunk名称=(.+?) ', alarm_desc)
    # alarm_port2 = _find(r'接口名称=(.+) ', alarm_desc)
    # alarm_port3 = _find(r'端口名称=(.+) ', alarm_desc)
    # alarm_port_desc = _find(r'别名=(.+) ', alarm_desc)
    alarm_info = _find(r'定位信息：(.+)端口备注', alarm_desc)
    return '\n\n> '.join([alarm_title, alarm_time, alarm_info+';'])
    return '\n\n> '.join([alarm_title, alarm_dev, alarm_ip, alarm_time, alarm_port1, alarm_port2, alarm_port3, alarm_port_desc, alarm_info])


def back(browser: WebDriver) -> None:
    '''
    跳转到最后打开的标签页
    '''
    browser.switch_to.window(browser.window_handles[-1])


def open_in_newtab(browser: WebDriver, url='') -> WebDriver:
    '''
    在新标签页打开网址
    '''
    time.sleep(1)
    back(browser)
    browser.execute_script('open("'+url+'")')
    back(browser)
    time.sleep(1)
    # browser.get(url)
    return browser


def wait_for_frame_document_ready(browser: WebDriver, frame_id='') -> None:
    '''
    等待 frame 加载完毕
    '''
    time.sleep(1)
    browser.switch_to.frame(frame_id)
    for i in range(20):
        if browser.execute_script("return document.readyState") == "complete":
            break
        else:
            time.sleep(1)
    browser.switch_to.default_content()
    return


def auto_reply_NOTICE(browser: WebDriver) -> int:
    '''
    回复（通知）工单的操作
    '''
    total = 0
    todo_list_url = 'http://10.204.137.51/eoms/wait/?baseSchema=WF4_EL_TTM_TTH_NOTICE#/'
    open_in_newtab(browser, todo_list_url)
    basesn = ''
    while True:
        back(browser)
        trs = browser.find_elements(By.CSS_SELECTOR, 'tbody tr')
        if len(trs) == 0:
            break
        trs[0].click()
        time.sleep(1)
        back(browser)
        # basesn1 = browser.find_element(By.ID, 'bpp_BaseSN').text
        # if basesn == basesn1:
        #     continue
        # else:
        #     basesn = basesn1
        wait = WebDriverWait(browser, 10)
        wait.until(EC.visibility_of_element_located(
            (By.ID, 'DealInfoViewField_bpp')))
        browser.find_element(By.ID, 'bpp_Btn_T1Finish').click()
        wait.until(EC.visibility_of_element_located(
            (By.ID, 'DealDesc'))).send_keys('已知晓。')
        wait_for_frame_document_ready(browser, 'DealInfoViewField')
        browser.execute_script('ActionPanel.submit();')
        total += 1
        time.sleep(3)

    browser.close()
    back(browser)
    return total


def is_element_exist(browser: WebDriver, css_selector):
    try:
        return browser.find_element(By.CSS_SELECTOR, css_selector)
    except:
        return False


def auto_reply_EQU(browser: WebDriver) -> list:
    '''
    回复（设备）工单的操作
    '''
    total = 0
    details = []
    todo_list_url = 'http://10.204.137.51/eoms/wait/?baseSchema=WF4_EL_TTM_TTH_EQU#/'
    open_in_newtab(browser, todo_list_url)
    offset = 0
    while True:
        back(browser)
        browser.execute_script('window.scrollTo(0, '+str(87*(offset+1))+');')
        trs = browser.find_elements(By.CSS_SELECTOR, 'tbody tr')
        if len(trs) - offset == 0:
            # 列表为空或仅剩未上清除时间的单子，则结束循环
            break
        if not '[数据网]' in trs[offset].text:
            # 跳过非[数据网]的工单
            offset += 1
            continue
        try_func(trs[offset].click(), True)
        time.sleep(1)
        back(browser)
        # browser.execute_script('window.scrollTo(0, 5000);')
        # 受理
        btn_accept = is_element_exist(browser, '#bpp_Btn_ACCEPT')
        if btn_accept:
            btn_accept.click()
            time.sleep(8)
            continue
        # 延期处理
        if is_element_exist(browser, '#INC_IsApplyResult'):
            browser.execute_script('F("INC_IsApplyResult").S("是");')
            browser.execute_script(
                'window.showModalDialog=function(){};ActionPanel.submit();')
            time.sleep(3)
            continue
        # 回复
        wait = WebDriverWait(browser, 5)
        _clear_time = wait.until(EC.visibility_of_element_located(
            (By.ID, 'INC_Alarm_ClearTime'))).get_attribute('value')
        _deal_out_time = browser.find_element(By.ID,
                                              'BaseDealOutTime').get_attribute('value')
        if _clear_time != '':
            browser.execute_script('window.alert=function(){};')
            if (datep(_deal_out_time)-datetime.now()).total_seconds() < 0:
                # 处理时限 < 当前时间，则延期
                browser.find_element(By.ID, 'bpp_Btn_T2Apply').click()
                browser.find_element(By.ID, 'INC_ApplyDesc').send_keys('申请延期')
                browser.execute_script(
                    'window.showModalDialog=function(){};ActionPanel.submit();')
                time.sleep(3)
                continue
            browser.find_element(By.ID, 'bpp_Btn_T2Finish').click()
            wait.until(EC.visibility_of_element_located(
                (By.ID, 'FromAlarmClearTime')))
            browser.execute_script(
                'F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("传输原因");F("FinishDealDesc").S("传输链路闪断造成");F("DealGuomodo").S("检查线路传输质量");F("isHomeService").S("否");F("fault_recover").S("彻底恢复");')
            browser.execute_script(
                'window.showModalDialog=function(){};ActionPanel.submit();')
            # browser.find_element(By.CSS_SELECTOR, 'div.confirm button').click()
            total += 1
            time.sleep(3)
        else:
            # 未上清除时间，获取工单详细信息
            detail = getOrderDetails(browser)
            details.append(detail)
            back(browser)
            offset += 1
            browser.close()
            print('未上清除累计：', offset)
        time.sleep(3)
    browser.close()
    back(browser)
    return [total, details]


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
        browser = getBrowser(exe)
        autoLogin(browser)
        jumpToEOMS(browser)
        try:
            _notice_num = auto_reply_NOTICE(browser)
        except Exception as err:
            print(err)
        try:
            _equ_num, details = auto_reply_EQU(browser)
        except Exception as err:
            print(err)
        total = len(details)
        details = '\n\n'.join(details) if not details == [] else '(空)'
        msg_title = '已自动回复设备故障工单 {} 个，通知工单 {} 个。未上清除{}个。'
        msg_title = msg_title.format(_equ_num, _notice_num, total)
        msg_content = '### [数据网]{}\n\n> 推送时间：{}\n\n**详细信息**：\n\n> {}'
        msg_content = msg_content.format(msg_title, datef(), details)
        send_msg(msg_markdown(msg_title, msg_content, True))
        browser.switch_to.default_content()
        browser.quit()
        print('* 当前时间：', datef())
        t = Timer(inc, loop, (inc,))
        t.start()
    loop(3600)
    # exit()
