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
from selenium.webdriver.chrome.service import Service
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
from win10toast import ToastNotifier

configFile = 'config.work.ini'
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


def datef(x=None) -> str:
    '''返回时间文本'''
    if x == None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return x.strftime("%Y-%m-%d %H:%M:%S")


'''时间类'''
def datep(x) -> datetime: return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')


def log(_str, file_name='eoms_auto_running.log'):
    '''
    输入到屏幕及文件
    '''
    print(_str)
    _str = str(_str).replace('\n\n', '\n') # 优化 markdown 格式的双换行
    with open(file_name, 'a') as f:
        f.write(_str)
        f.write('\n')


def pauseAndExit(text=''):
    print(text)
    os.system('pause')
    sys.exit()


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
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    if '-w' in args:
        options.add_argument("--window-size=1920,3000")
        options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('blink-settings=imagesEnabled=false')
    _service = Service(exe)
    if browser_type == 'ie':
        return webdriver.Ie(service=_service)
    if browser_type == 'chrome':
        return webdriver.Chrome(options=options, service=_service)


def autoLogin(browser: WebDriver, keepalive=False) -> WebDriver:
    uip_url = 'http://uip.ln.cmcc/'
    browser.get(uip_url)
    if 'Login' not in browser.current_url:
        return browser

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
    if keepalive:
        # 10min
        loopRefresh(611, browser.window_handles[0], uip_url)
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
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, _selector)))
    # browser.get('http://10.204.137.51/eoms/')
    return browser


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


def getOrderDetail(browser: WebDriver) -> list:
    '''
    return [detail, extra] -> [list(), str()]
    '''
    alarm_desc = browser.find_element(By.ID, 'INC_Alarm_Desc').text
    base_sn = browser.find_element(By.ID, 'bpp_BaseSN').text  # 工单号
    alarm_sn = browser.find_element(By.ID, 'INC_Alarm_SN').get_attribute('value')  # 告警流水号
    alarm_origin_id = browser.find_element(By.ID, 'INC_Alarm_OriAlarmId').get_property('value')  # 原始告警号
    # extra = '工单号 {}\n\n告警流水号 {}\n\n原始告警号 {}'.format(base_sn, alarm_sn, alarm_origin_id).split('\n\n')
    _date = datetime.now().strftime("%Y-%m-%d")
    extra = '{}\t{}\t{}\t铁岭\t城域网\t批量工单无清除时间\t{}'.format(_date, base_sn, alarm_sn, alarm_origin_id)

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
    alarm_info = _find(r'定位信息：(.+).\n附加信息', alarm_desc)
    if alarm_info == '':
        alarm_info = _find(r'告警详情：\n([\s\S]+)', alarm_desc)
    elif alarm_info == '':
        alarm_info = _find(r'告警标题 = ([\s\S]+)', alarm_desc)
    elif alarm_info == '':
        alarm_info = alarm_desc
    alarm_info = alarm_info.replace(' ', '_').replace('](', '_').replace('\n', ' \n')  # 为了转成 markdown 美观
    # return '\n\n> '.join([alarm_title, alarm_time, alarm_info, *extra, ';']), alarm_origin_id
    return '\n> '.join([alarm_title, alarm_time, alarm_info, ';']), extra


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
    _notice_num = 0
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
        wait.until(EC.visibility_of_element_located((By.ID, 'DealInfoViewField_bpp')))
        browser.find_element(By.ID, 'bpp_Btn_T1Finish').click()
        wait.until(EC.visibility_of_element_located((By.ID, 'DealDesc'))).send_keys('已知晓。')
        wait_for_frame_document_ready(browser, 'DealInfoViewField')
        browser.execute_script('ActionPanel.submit();')
        _notice_num += 1
        time.sleep(3)

    browser.close()
    back(browser)
    return _notice_num


def is_element_exist(browser: WebDriver, css_selector):
    try:
        return browser.find_element(By.CSS_SELECTOR, css_selector)
    except:
        return False


def get_uncleared_ids():
    '''
    获取未上清除时间的单子（已发邮件）
    '''
    id_list = []
    try:
        with open('cleared.txt', 'r') as f:
            ids = f.readline()[:-1]
        id_list = ids.split(';')
    except:
        ...
    return id_list


def auto_reply_EQU(browser: WebDriver) -> list:
    '''
    回复（设备）工单的操作
    '''

    def delay(browser: WebDriver):
        '''
        延期操作
        '''
        print('申请延期', end=',,')
        browser.find_element(By.ID, 'bpp_Btn_T2Apply').click()  # 点击申请延期按钮
        wait.until(EC.visibility_of_element_located((By.ID, 'INC_ApplyDesc'))).send_keys('申请延期')
        # browser.find_element(By.ID, 'INC_ApplyDesc').send_keys('申请延期')
        browser.execute_script('window.showModalDialog=function(){};ActionPanel.submit();')
        print('提交延期完成')

    def reply(browser, force=False):
        '''
        正常回单
        '''
        print('正常回单', end=',,')
        if not is_element_exist(browser, '#FromAlarmClearTime'):
            browser.find_element(By.ID, 'bpp_Btn_T2Finish').click() # 点击完成处理按钮
            wait.until(EC.visibility_of_element_located((By.ID, 'FromAlarmClearTime'))) # 告警消除时间来源（左下角）
        if force:
            # 强制输入当前时间为清除时间进行回单
            date_str = datef()
            browser.execute_script('F("ClearINCTime").S("{}");'.format(date_str))
        browser.execute_script(
            'F("tth_region").S("农村");F("ReasonType").S("数通设备");F("ReasonSubType").S("传输原因");F("FinishDealDesc").S("传输链路闪断");F("DealGuomodo").S("闪断后自动恢复");F("isHomeService").S("否");F("fault_recover").S("彻底恢复");')
        # browser.find_element(By.CSS_SELECTOR, 'div.confirm button').click()
        browser.execute_script('window.showModalDialog=function(){};ActionPanel.submit();')
        print('提交回单完成')
        time.sleep(2)

    def reply_or_delay(browser):
        '''
        正常回单或延期操作
        '''
        browser.execute_script('window.alert=function(){};')
        browser.execute_script('ActionPanel.goBack();')
        if (datep(_deal_out_time)-datetime.now()).total_seconds() < 0:
            # 处理时限 < 当前时间，则延期
            delay(browser)
        else:
            reply(browser)
        time.sleep(2)

    num_accept, num_equ, num_equ2 = 0, 0, 0
    details = []  # 未上清除工单的详细信息
    extras = ['']  # U2000 查找以及发邮件所需的信息
    todo_list_url = 'http://10.204.137.51/eoms/wait/?baseSchema=WF4_EL_TTM_TTH_EQU#/'
    open_in_newtab(browser, todo_list_url)
    offset = 0
    while True:
        back(browser)
        browser.execute_script('window.scrollTo(0, '+str(87*(offset))+');')
        trs = browser.find_elements(By.CSS_SELECTOR, 'tbody tr')
        if len(trs) - offset == 0:
            # 列表为空或仅剩未上清除时间的单子，则结束循环
            break
        if not '[数据网]' in trs[offset].text:
            # 跳过非[数据网]的工单
            offset += 1
            continue
        try:
            trs[offset].click()
        except Exception as err:
            print('ERR: ', err)
            send_msg(msg_text('ERR:{}'.format(err)))
            browser.refresh()
            continue
        time.sleep(1)
        back(browser)
        # browser.execute_script('window.scrollTo(0, 5000);')
        # 受理
        btn_accept = is_element_exist(browser, '#bpp_Btn_ACCEPT')
        if btn_accept:
            btn_accept.click()
            num_accept += 1
            time.sleep(8)
            continue
        # 延期处理
        if is_element_exist(browser, '#INC_IsApplyResult'):
            print('延期审批', end=',,')
            browser.execute_script('F("INC_IsApplyResult").S("是");')
            browser.execute_script('window.showModalDialog=function(){};ActionPanel.submit();')
            time.sleep(5)
            print('完成延期')
            continue
        # 回复
        wait = WebDriverWait(browser, 5)
        _clear_time = wait.until(EC.visibility_of_element_located((By.ID, 'INC_Alarm_ClearTime'))).get_attribute('value')
        _deal_out_time = browser.find_element(By.ID, 'BaseDealOutTime').get_attribute('value')
        if _clear_time != '':
            # 已上清除时间，正常回单、二次回单或延期操作
            if '质检' in browser.find_element(By.CLASS_NAME, 'basestatus').text:
                # 二次回单
                num_equ2 += 1
                browser.close()
                continue  # 本次 while 循环结束进入下一轮
            print('已上清除，正常回单或延期', end=',,')
            reply_or_delay(browser)
            num_equ += 1
            time.sleep(3)
        else:
            # 未上清除时间，手动获取一次
            print('未上清除，手动获取一次', end=',,')
            browser.execute_script('window.showModalDialog=function(){};window.alert=function(){};')
            browser.find_element(By.ID, 'bpp_Btn_T2Finish').click()  # 点击完成处理按钮
            wait.until(EC.visibility_of_element_located((By.ID, 'FromAlarmClearTime')))
            browser.find_element(By.ID, 'queryClearTime_bt1').click()  # 点击获取告警清除时间按钮
            _flag = False
            for x in range(10):
                if browser.find_element(By.ID, 'INC_Alarm_ClearTime').get_attribute('value') != '':
                    # 若手动获取清除时间成功，则继续回单或延期
                    print('手动获取清除时间成功，继续回单或延期', end=',,')
                    reply_or_delay(browser)
                    num_equ += 1
                    time.sleep(3)
                    _flag = True
                    break   # 退出 for 循环
                time.sleep(0.5)
            if _flag:
                continue  # 本次 while 循环结束进入下一轮
            # 未上清除时间，且手动获取不到，获取工单详细信息
            print('未上清除，获取详情', end=',,')
            detail, extra = getOrderDetail(browser)
            _, base_sn, _, _, _, _, alarm_origin_id = extra.split('\t')
            if alarm_origin_id in get_uncleared_ids():
                # 未上清除时间的工单若已发邮件，则可以强制回单
                print('识别到已发邮件告知，执行强制回单：{}'.format(base_sn))
                reply(browser, True)
                num_equ += 1
                time.sleep(3)
                continue  # 本次 while 循环结束进入下一轮
            # 整理详情，用于发推送
            details.append(detail)
            extras[0] = extras[0] + alarm_origin_id + ';'
            extras.append(extra)
            print('成功获取详情')
            back(browser)
            offset += 1
            browser.close()
            print('未上清除累计：{}\r'.format(len(extras)-1), end='')
        time.sleep(3)
    browser.close()
    back(browser)
    return [num_accept, num_equ, num_equ2, details, extras]


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


def show_toast(toast, title, text):
    '''
    发送 win10 本地推送
    '''
    while toast.notification_active:
        time.sleep(1)
    ico = 'D:\\home\\xda-scripts-user-js\\__favicon\\fav1.ico'
    toast.show_toast(title, text, icon_path=ico, threaded=True)


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
        print('推送DingTalk异常！')
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
    log('------------msg_markdown----start-----')
    log(title)
    log('------------title above----text below-')
    log(text)
    log('------------msg_markdown-----end------')
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


def loop(browser, inc, count, num_a, num_e2, num_e, num_n):
    '''
    循环体，自动回单
    '''
    _accept_num, _equ_num, _num_equ2, details, extras, _un_clear = 0, 0, 0, [], '', 0
    if count % 9 == 0:
        autoLogin(browser)
    try:
        back(browser)
        jumpToEOMS(browser)
        _notice_num = auto_reply_NOTICE(browser)
        print()
        _accept_num, _equ_num, _num_equ2, details, extras = auto_reply_EQU(browser)
    except Exception as err:
        print(err)
    browser.switch_to.default_content()
    # browser.quit()
    print('* 当前时间：{}，Loop：{}'.format(datef(), count), end='')
    count -= 1
    num_a += _accept_num
    num_e += _equ_num
    num_e2 += _num_equ2
    num_n += _notice_num
    if count == 0:
        msg_title = '设备故障工单'
        if num_a > 0:
            msg_title += '受理 {} 个。'.format(num_a)
        if num_e > 0:
            msg_title += '回复 {} 个。'.format(num_e)
        if num_n > 0:
            msg_title += '通知工单回复 {} 个。'.format(num_n)
        if _num_equ2 > 0:
            msg_title += '需二次回单 {} 个。'.format(_num_equ2)
        msg_content = '### [数据网]{}\n\n> 推送时间：{}'
        if details != []:
            print('')
            _un_clear = len(details)
            msg_title += '未上清除 {} 个。'.format(_un_clear)
            details = '\n\n'.join(details)
            send_msg(msg_markdown('未上清除详细信息', '\n\n'.join(extras)))
            msg_content += '\n\n#### 详细信息：\n\n {}'.format(details)
        msg_content = msg_content.format(msg_title, datef())
        send_msg(msg_markdown(msg_title, msg_content, True))
        toast = ToastNotifier()
        toast.show_toast(msg_title, msg_content, threaded=True)
        count = 55
        num_a, num_e, num_e2, num_n = 0, 0, 0, 0
    t = Timer(inc, loop, (browser, inc, count, num_a, num_e, num_e2, num_n))
    t.start()


if __name__ == "__main__":
    ...
    browser = getBrowser(exe)
    autoLogin(browser)
    count = 1
    num_a, num_e, num_e2, num_n = 0, 0, 0, 0
    loop(browser, 60, count, num_a, num_e, num_e2, num_n)
    # exit()
