from selenium import webdriver
import time
import configparser
from selenium.webdriver.common.keys import Keys
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

#成功与失败计数
success = 0
fail = 0

def post_delete(mid,header):
    form = {
        "mid":mid
    }
    r = requests.post("https://weibo.com/aj/mblogpq/del?ajwvr=6https://weibo.com/aj/mblog/del?ajwvr=6",data=form,headers=header)
    if r.json().get('code') == '100000':
        global success
        success = success + 1
        return f'{mid}删除成功'
    else:
        global fail
        fail = fail + 1
        return f'{mid}删除失败'

if __name__ == '__main__':
    #读取配置文件
    config = configparser.ConfigParser()
    config.read('D:\py\weibo_account.ini','utf-8-sig')
    account = config['weibo']['account']
    password = config['weibo']['password']
    driver = webdriver.Chrome('D:/Github/python-practice/chromedriver/2.41/chromedriver.exe')
    driver.maximize_window()
    driver.implicitly_wait(10) # seconds
    driver.get("http://weibo.com")
    driver.find_element_by_id('loginname').send_keys(account)
    # driver.find_element_by_id('loginname').send_keys(Keys.TAB)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_class_name('W_btn_a').click()
    try:
        verifycode_input = driver.find_element_by_name('verifycode')
        verifycode = input('请手动输入验证码：')
        driver.find_element_by_name('verifycode').send_keys(verifycode)
        driver.find_elements_by_class_name('W_btn_a').click()
    except:
        pass
    finally:
        time.sleep(15)
        print('登录成功')
        cookie = [f'{cookie["name"]}={cookie["value"]}' for cookie in driver.get_cookies()]
        # 获取cookies
        cookies = ";".join(cookie)
        print("获取cookies成功")
        print(cookies)
        mid = '3857920662257336'
        header = {
            "Accept":"*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "20",
            "Content-Type":"application/x-www-form-urlencoded",
            "Cookie":cookies,
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Host":"weibo.com",
            "Origin":"https://weibo.com",
            "Referer":"https://weibo.com/baka05/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1",
            "X-Requested-With":"XMLHttpRequest"
        }
        # 读取mid并删除
        form = {
            "mid":mid
        }
        r = requests.post("https://weibo.com/aj/mblogpq/del?ajwvr=6https://weibo.com/aj/mblog/del?ajwvr=6",data=form,headers=header)
        print(r.json())
        # if r.json().get('code') == '100000':
        # with open('D:\Github\python-practice\selenium练习\mids.txt') as midslist:
        #     mids = list(map(lambda m : m.replace('\n',''),midslist))