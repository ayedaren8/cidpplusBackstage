from ehall.Spider import Spider
from ehall.SpiderJw import SpiderJw
from requests.cookies import RequestsCookieJar
import requests
import json


class SpiderPost(SpiderJw, Spider):
    "教务衍生爬虫，用于处理教务管理系统的部分请求"
    def __init__(self, url, username, password, data):
        super().__init__(url=url, username=username, password=password)
        self.url = url
        self.data = data

    def grep(self):
        # print("SpiderPost爬虫")
        try:
            driver = self.driver
            cookies = driver.get_cookies()
            driver.quit()
            jar = RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            se = requests.session()
            se.cookies.update(jar)
            res = se.post(
                url=self.url, data=self.data)
            self.res = json.loads(res.text)
        except Exception as e:
            self.error="pwdError"
            print(e)

    def sendBack(self):
        self.res = self.res
