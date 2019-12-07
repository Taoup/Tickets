# coding: utf-8
from json import loads
import os
import pickle
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import my_print


def login(nick_name):
    _login(nick_name)
    _double_check_login(nick_name)

    # prefs = {"profile.managed_default_content_settings.images":2}
    # prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
    # options.add_experimental_option("prefs",prefs)
    # global driver
    # driver = webdriver.Chrome(options=options)


def _login(nick_name, cookie_file = 'cookies.pkl', url = "https://www.damai.cn/"):
    driver.get(url)
    if os.path.exists(cookie_file):
        with open(cookie_file, 'rb') as t:
            cookies = pickle.load(t)
            for c in cookies:
                if 'expiry' in c:
                    del c['expiry']
                c['expires'] = ""
                driver.add_cookie(c)
    else:
        while True:
            my_print("请从自行从打开的网页进行登录")
            tmp =  driver.find_elements_by_class_name("span-box-header")
            if nick_name in [i.text for i in tmp if hasattr(i, 'text')]:
                break
            sleep(3)
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        

def _double_check_login(nick_name, cookie_file = 'cookies.pkl', url = "https://www.damai.cn/"):
    #扫码登录或者加载cookie成功，检查是否真的登录成功。
    driver.get(url)
    tmp =  driver.find_elements_by_class_name("span-box-header")
    if nick_name not in [i.text for i in tmp if hasattr(i, 'text')]:
        my_print(f'登录失败，删除{cookie_file},重试中...')
        os.remove(cookie_file)
        _login(nick_name)

    my_print("登录成功")

    
def order(target, city, date, price, num_tickets, refresh_interval = 0.5):
    driver.get(target)
    buybtn = driver.find_element_by_class_name("buybtn")
    while "即将" in buybtn.text:
        my_print("还未开售，疯狂刷新中...")
        sleep(refresh_interval)
        driver.refresh()
        buybtn = driver.find_element_by_class_name("buybtn")

    # 选择城市，有的抢票可能没有这个选项
    if city:
        city_elements = driver.find_elements_by_class_name('cityitem')
        for wo in city_elements:
            if hasattr(wo, 'text') and city in wo.text:
                wo.click()
                break

    # 选择时间场次
    date_elements = driver.find_elements_by_class_name('select_right_list_item')
    for d in date_elements:
        if hasattr(d, 'text') and date in d.text:
            d.click()
            break
    
    #选择价位
    price_elements = driver.find_elements_by_class_name('select_right_list_item')
    for p in price_elements:
        if hasattr(p, 'text') and price in p.text:
            p.click()
            break
    
    # 选择数量 or 选座购票
    num_elem = driver.find_element_by_class_name('cafe-c-input-number-input')
    num_elem.clear()
    num_elem.send_keys(num_tickets)

    #下单
    buybtn = driver.find_element_by_class_name("buybtn")
    buybtn.click()


def confirm_order(audiences):
    """
    从前一步下单，到这一步确认订单，在抢票忙时链接的跳转可能会比较耗时，
    这里可能要考虑下鲁棒性。
    """    
    candidates = driver.find_elements_by_class_name("next-checkbox-label")
    as_least_one = False
    for who in audiences:
        for web_object in candidates:
            if who in web_object.text:
                web_object.click()
                as_least_one = True
    if not as_least_one:
        raise Exception("确认订单时，没有任何观众被选中，请尽快检查")

    #支付方式，目前看到的默认支付宝

    #确定下单
    confirm_btn = driver.find_element_by_css_selector(".submit-wrapper .next-btn")
    if __debug__:
        confirm_btn.click()
    global success
    success = True
    my_print("抢票成功，请自行支付")        


success = False

options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.implicitly_wait(5)


if __name__ == '__main__':

    """test code here"""
