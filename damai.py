# coding: utf-8
import json
import os
import pickle
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import my_print


class GoDamai:
    def __init__(self, browser = 'chrome', debug = False):
        self.debug = debug
        if browser == 'chrome':
            self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)      #没找到元素会等待5s，5s后还是没有找到该元素才抛出异常。
        self.name = 'damai'
        selectors_file = f'{self.name}_{browser}.json'
        self.selectors = json.load(open(os.path.join('resources', selectors_file), 'r'))
        self.success = False

    def login(self, nick_name):
        self._login(nick_name)
        self._double_check_login(nick_name)


    def _login(self, nick_name, cookie_file = 'cookies.pkl', url = "https://www.damai.cn/"):
        self.driver.get(url)
        if os.path.exists(cookie_file):
            with open(cookie_file, 'rb') as t:
                cookies = pickle.load(t)
                for c in cookies:
                    if 'expiry' in c:
                        del c['expiry']
                    c['expires'] = ""
                    self.driver.add_cookie(c)
        else:
            while True:
                my_print("请从自行从打开的网页进行登录")
                tmp = self.driver.find_elements_by_css_selector(self.selectors['login'])
                if nick_name in [i.text for i in tmp if hasattr(i, 'text')]:
                    break
                sleep(3)
            pickle.dump(self.driver.get_cookies(), open(cookie_file, "wb"))
            

    def _double_check_login(self, nick_name, cookie_file = 'cookies.pkl', url = "https://www.damai.cn/"):
        #扫码登录或者加载cookie成功，检查是否真的登录成功(有时候加载cookies登录失败)。
        self.driver.get(url)
        tmp = self.driver.find_elements_by_css_selector(self.selectors['login'])
        if nick_name not in [i.text for i in tmp if hasattr(i, 'text')]:
            my_print(f'登录失败，请检查昵称是否正确， 我会删除{cookie_file}并重试...')
            os.remove(cookie_file)
            self._login(nick_name)

        my_print("登录成功")

        
    def order(self, target, city, date, price, num_tickets, refresh_interval = 0.5):
        self.driver.get(target)
        buybtn = self.driver.find_element_by_css_selector(self.selectors['buy_btn'])
        while "即将" in buybtn.text:
            my_print("还未开售，疯狂刷新中...")
            sleep(refresh_interval)
            self.driver.refresh()
            buybtn = self.driver.find_elements_by_css_selector(self.selectors['buy_btn'])

        # 选择城市，有的抢票可能没有这个选项
        if city:
            city_elements = self.driver.find_elements_by_css_selector(self.selectors['city'])
            for wo in city_elements:
                if hasattr(wo, 'text') and city in wo.text:
                    wo.click()
                    break

        # 选择时间场次
        date_elements = self.driver.find_elements_by_css_selector(self.selectors['date'])
        
        for d in date_elements:
            if hasattr(d, 'text') and date in d.text:
                my_print(f"选择场次：{d.text}")
                d.click()
                break
        
        #选择价位
        price_elements = self.driver.find_elements_by_css_selector(self.selectors['price'])
        for p in price_elements:
            if hasattr(p, 'text') and price in p.text:
                my_print(f"选择价位:{p.text}")
                p.click()
                break
        
        # 选择数量 or 选座购票
        num_elem = self.driver.find_element_by_css_selector(self.selectors['num_tickes'])
        num_elem.clear()
        my_print(f"购票数量:{num_tickets}")
        num_elem.send_keys(num_tickets)

        #下单
        buybtn = self.driver.find_element_by_css_selector(self.selectors['buy_btn'])
        buybtn.click()


    def confirm_order(self, audiences):
        buyer_select = self.driver.find_elements_by_css_selector(self.selectors['buyer_select'])
        if len(buyer_select) != 0:
            # 需要选择购票人
            my_print("选择购票人中。。。")
            candidates = self.driver.find_elements_by_css_selector(self.selectors['audiences'])
            # print([i.text for i in candidates])
            as_least_one = False
            for who in audiences:
                for web_object in candidates:
                    if who in web_object.text:
                        # BUG: 可能会没有选中！！！
                        web_object.click()
                        my_print(f"选中购票人：{web_object.text}")
                        as_least_one = True
            if not as_least_one:
                raise Exception("确认订单时，没有任何观众被选中，请尽快检查")

        #支付方式，目前看到的默认支付宝

        #确定下单
        confirm_btn = self.driver.find_element_by_css_selector(self.selectors['confirm_btn'])
        if not self.debug:
            confirm_btn.click()

        self.success = True
        my_print("抢票成功，请自行支付")        



target_url = """
https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.f19423e1kLhjcU&id=609134671437 """

if __name__ == '__main__':
    target_url = target_url.strip()

    go = GoDamai(debug = True)

    go.login(nick_name = '麦子')

    go.order(target = target_url,          #抢票页面的url
            city = None,              #不用选择城市的场次，city传入None
            date = '2020',        
            price = '880', 
            num_tickets = 2)
    go.confirm_order(audiences = ['马宏涛', 'xxx'])