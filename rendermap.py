from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

from config import config, baidu

url = 'http://' + config['host'] + ':' + \
    str(config['port']) + '/static/historyMap.html'

dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0")

print('Init PhantomJS...')
# driver = webdriver.Remote(command_executor=config['phantomjs-url'], desired_capabilities=dcap)
driver = webdriver.Remote(command_executor='http://127.0.0.1:8910', desired_capabilities=dcap)
driver.set_page_load_timeout(300)
driver.set_window_size(800, 600)
print('Init PhantomJS done')
page_loaded = False


def load_page():
    print('load render page...' + url)
    driver.get(url)
    print('load render page done')
    # print((driver.page_source).encode('gbk'))


def webscreen(entity_name, start, end):
    load_page()
    baidu_init_js = "ak = '" + baidu['ak'] + \
        "';serviceId = '" + baidu['serviceid'] + "'"
    js = "render('" + entity_name + "'," + start + "," + end + ")"
    print('execute js: ' + js)
    driver.execute_script(baidu_init_js)
    driver.execute_script(js)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "done"))
    )
    print('js executed.')
    time.sleep(1)

    png = driver.get_screenshot_as_png()
    return png


def quit_driver():
    driver.quit()
