from xdaLibs import iniconfig
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def autoLogin(url):
    configFile = 'config.work.ini'
    conf = iniconfig.IniConfig(configFile)

    username = conf.get('UIP','u')
    password = conf.get('UIP','p')
    exe = conf.get('common','exe')
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Ie(executable_path=exe)
    browser.get(url)
    browser.find_element(By.ID,'userName').send_keys(username)
    browser.find_element(By.CSS_SELECTOR,'div.bttn a').click()
    wait = WebDriverWait(browser, 300)
    wait.until(EC.visibility_of_element_located((By.ID,'smsPwd'))).send_keys(password)
    browser.find_element(By.ID,'sendsms_btn').click()
    # browser.execute_script('jkManageSMS()')
    print('输入验证码后点击登录。\n此操作等待 5 分钟。')

    browser.execute_script("arguments[0].focus();",browser.find_element(By.ID,'dynamic_smsPwd'))
    # browser.find_element(By.CSS_SELECTOR,'div.bttn a.loginbtn').click()
    # browser.execute_script('smsLogin()')
    wait.until(EC.visibility_of_element_located((By.ID, "chromemenu")))
    print('已检测到登录成功，继续操作')
    # menuUrl = '/page/resgroup/left.jsp'
    # browser.maximize_window()
    # browser.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')
    browser.implicitly_wait(10)

    """打开对应的三级节点"""
    nodes = conf.listOptions('4A')
    flag = 0
    for x in nodes:
        if flag:
            browser.execute_script('window.open("'+browser.current_url+'")')
            browser.switch_to.window(browser.window_handles[-1])
        openNode(browser, x)
        flag +=1


"""打开到指定三级节点"""
def openNode(browser, node='CMNET城域网'):
    browser.switch_to.default_content()
    browser.switch_to.frame('content')
    browser.switch_to.frame('leftFrame')
    wait = WebDriverWait(browser, 10)
    menuEle = browser.find_element(By.CSS_SELECTOR,'div#resgroupTree table:nth-child(1)')
    selector = 'tr:nth-child(1) td:nth-child(1)'

    """点击 地市公司"""
    cityEle = menuEle.find_element(By.CSS_SELECTOR,'table:nth-child(1) table:nth-child(1)')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,selector)))
    cityEle.find_element(By.CSS_SELECTOR,selector).click()

    """点击 铁岭公司"""
    tieling = cityEle.find_element(By.CSS_SELECTOR,'tr:nth-child(2) table:nth-child(1)')
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,selector)))
    tieling.find_element(By.CSS_SELECTOR,selector).click()

    group = tieling.find_elements(By.CSS_SELECTOR,'tr td span')
    for x in group:
        if x.text == node:
            nd = x
    nd.click()

    """按设备名称排序"""
    browser.switch_to.default_content()
    browser.switch_to.frame('content')
    browser.switch_to.frame('contentFrame')
    wait.until(EC.visibility_of_element_located((By.ID,'amsgrid_bodyDiv')))
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR,'div#amsgrid table#amsgrid_headTable tr:nth-child(1) td:nth-child(2)').click()


if __name__ == "__main__":
    t0 = time.time()
    url = 'http://4aportal.ln.cmcc/'
    autoLogin(url)
    t = time.time()-t0
    print('\n执行完毕，用时：%2.4f s' % t)
    print('Have fun...')