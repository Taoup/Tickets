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


def login(url = "https://www.damai.cn/", cookie_file = 'cookies.pkl'):
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
            my_print("请登录")
            tmp =  driver.find_elements_by_class_name("span-box-header")
            if loggin_user_name in [i.text for i in tmp]:
                break
            sleep(3)
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        

def double_check_login(cookie_file = 'cookies.pkl'):
    #扫码登录或者加载cookie成功，检查是否真的登录成功。
    driver.get(target_url)
    diff_of_2types = ["div[3]/div[1]/a[2]/div", "ul/li[2]/div/label/a[2]"]
    locator = (By.XPATH, "/html/body/div[1]/div/" + diff_of_2types['detail' not in target_url])
    try:
        WebDriverWait(driver, 3, 0.3).until(
            EC.text_to_be_present_in_element(locator, loggin_user_name))
    except Exception as e:
        my_print(f'登录失败，删除{cookie_file},然后重试')
        os.remove(cookie_file)
        login()

    my_print("登录成功")

    

target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.4a3423e15XF1CC&id=608137824452"
driver = webdriver.Chrome()
loggin_user_name = '麦子'


if __name__ == '__main__':

    login()
    double_check_login()


    # order()

    # pay()

    # driver.quit()