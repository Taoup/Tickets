# coding: utf-8
from json import loads
import os
import pickle
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def my_print(msg):
    print("-" * 20 + msg + "-" * 20)


def login(url, nick_name = 'xxx', cookie_file = 'cookies.pkl'):
    driver.get(url)     #这个对后面add_cookie非常重要，没有会抛出invalidcookiedomainexception异常。
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
            my_print("请从打开的网页进行登录")
            tmp =  driver.find_elements_by_class_name("span-box-header")
            if nick_name in [i.text for i in tmp if hasattr(i, 'text')]:
                break
            sleep(3)
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        

def double_check_login(url, nick_name = 'xxx', cookie_file = 'cookies.pkl'):
    #扫码登录或者加载cookie成功，检查是否真的登录成功。
    driver.get(url)
    tmp =  driver.find_elements_by_class_name("span-box-header")
    if nick_name not in [i.text for i in tmp if hasattr(i, 'text')]:
        my_print(f'登录失败，删除{cookie_file},重试中...')
        os.remove(cookie_file)
        login()

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
        try:
            city_elements = driver.find_elements_by_class_name('cityitem')
            for wo in city_elements:
                if hasattr(wo, 'text') and city in wo.text:
                    wo.click()
                    break
        except Exception as e:
            my_print('不用选择城市，继续...')

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
    try:
        num_elem = driver.find_element_by_class_name('cafe-c-input-number-input')
    except Exception:
        my_print("目前无法自动选座，后续操作请自行进行...")
        exit(0)    
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
    for who in audiences:
        for web_object in candidates:
            if who in web_object.text:
                web_object.click()
    
    #支付方式，目前看到的默认支付宝

    #确定下单
    confirm_btn = driver.find_element_by_css_selector(".submit-wrapper .next-btn")
    if not DEBUG:
        confirm_btn.click()

    my_print("抢票成功，请自行支付")        


driver = webdriver.Chrome()
DEBUG = False

if __name__ == '__main__':

    home_page = "https://www.damai.cn/"
    target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.4a3423e15XF1CC&id=608137824452"

    login(url = home_page, nick_name = '麦子')
    double_check_login(url = home_page, nick_name = '麦子')

    order(target = target_url,          #抢票页面的url
            city = '无锡',              #不用选择城市的场次，city传入None
            date = '2020-01-01',        
            price = '内场1680元', 
            num_tickets = 2)

    confirm_order(audiences = ['马宏涛', 'xxx'])
