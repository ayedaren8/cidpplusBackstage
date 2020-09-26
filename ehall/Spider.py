import requests
from selenium import webdriver
import time
from requests.cookies import RequestsCookieJar


class Spider(object):
    "根爬虫，用于处理ehall大厅的部分请求"
    browser_path = "/hello/ehall/phantomjs"
    def __init__(self, username, password, url):
        self.open_url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html"
        self.url = url
        self.jar = None
        self.driver = None
        self.res = ''
        self.error= ''
        self.username = username
        self.password = password
        self.isNeedCap = None
        self.needCaptcha()

    def needCaptcha(self):
        ts = int(round(time.time() * 1000))
        url = "http://authserver.cidp.edu.cn/authserver/needCaptcha.html?username={username}&pwdEncrypt2=pwdEncryptSalt&_={ts}".format(
            username=self.username, ts=ts)
        res = requests.post(url)
        if res.text == "false":
            self.isNeedCap = False
        else:
            self.isNeedCap = True
            self.error="capError"

    def openBrowser(self):
        try:
            service_arg=[]
            service_arg.append('--load-images=no')#禁用图片
            service_arg.append('--disk-cache=yes')#开启缓存
            service_arg.append('--ignore-ssl-errors=true')#忽略https错误
            driver = webdriver.PhantomJS(executable_path=Spider.browser_path,service_args=service_arg)
            driver.set_page_load_timeout(10)#设置超时
            self.driver = driver
            return driver
        except Exception as e:
            print(e)
            self.error="driverError"

    def openRequest(self):
        try:
            driver = self.driver
            driver.get(url=self.open_url)
            driver.find_element_by_name('username').send_keys(self.username)
            driver.find_element_by_id('password').send_keys(self.password)
            driver.find_element_by_tag_name('button').click()
            cookies = driver.get_cookies()
            jar = RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            self.jar = jar
            # print("字典",self.jar)
        except Exception as e:
            print(e)
            self.error="findError"
        finally:
            driver.quit()

    def grep(self):
        res = requests.get(url=self.url, cookies=self.jar)
        if res.url == self.url:
            self.res = res
        else:
            self.error="pwdError"

    def check(self):
        if self.error != '':
            print(self.error)
        else:
            self.sendBack()

    def sendBack(self):
        # print(self.res.text)
        self.res = self.res.text

    def quit(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e)

    def run(self):

        if self.isNeedCap is False:
            self.openBrowser()
            self.openRequest()
            self.grep()
            self.check()
            return self.error, self.res
        else:
            print(self.error)
            return self.error, self.res
