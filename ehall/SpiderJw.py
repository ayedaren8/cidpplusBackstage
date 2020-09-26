#!/usr/bin/env python
# encoding: utf-8
from ehall.Spider import Spider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time


class SpiderJw(Spider):  
    "教务爬虫，用于处理教务管理系统的成绩部分"

    def __init__(self, username, password, url):
        self.url = url
        super().__init__(url=self.url, username=username, password=password)
        self.xueqi = ''
        self.chengji = ''
       

    def CHECK(fun):
        def inner(self, *args, **kwargs):
            if self.error is '':
                fun(self, *args, **kwargs)
            else:
                print(fun.__name__+"not run,because")
        return inner

    @CHECK
    def openRequest(self):
        # print("SpiderJw爬虫")
        url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"
        try:
            driver = self.driver
            driver.get(url=url)
            driver.find_element_by_name('username').send_keys(self.username)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_tag_name('button').click()
            self.driver = driver
        except Exception:
            self.error="findError"
            driver.quit()

    @CHECK
    def grep(self):
        driver = self.driver
        print(driver.title)
        try:
            WebDriverWait(driver,3).until(EC.title_is("教务管理系统"))
            driver.get(url=self.url)
            xueqi = driver.find_element_by_xpath(
                "//input[@id='hfSemesterFramework']")
            chengji = driver.find_element_by_xpath(
                "//input[@id='hfAverageMarkFromClass']")
            xueqi = xueqi.get_attribute("value")
            chengji = chengji.get_attribute("value")
            driver.quit()
            self.xueqi = json.loads(xueqi)
            self.chengji = json.loads(chengji)       
        except Exception as e:
            print(e)
            self.error="sysBusy"
            driver.quit()

    @CHECK
    def clear_Data(self):
        for year in self.xueqi:
            for i in year["List"]:
                gradeList = []
                for n in self.chengji:
                    if int(i["SemesterId"]) == int(n["SemesterID"]):
                        gradeList.append(n)
                i.update({"gradeList": gradeList})
        self.res = self.xueqi
        print('xueqi')

    @CHECK
    def sendBack(self):
        self.clear_Data()

    def run(self):
        if self.isNeedCap is False:
            self.openBrowser()
            self.openRequest()
            self.grep()
            self.check()
            self.quit()
            return self.error, self.res
        else:
            return self.error,self.res
