import re
import scrapy
from ..config import ZHIHU_PASSWORD, ZHIHU_PHONE

class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/search?type=content&q=python']

    def start_requests(self):
        from selenium import webdriver
        import time
        browser = webdriver.PhantomJS()

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(ZHIHU_PHONE)
        time.sleep(1)
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(ZHIHU_PASSWORD)
        time.sleep(2)
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(3)
        browser.get("https://www.zhihu.com/")
        time.sleep(6)
        zhihu_cookies = browser.get_cookies()
        cookie_dict = {}
        import pickle
        for cookie in zhihu_cookies:
            f = open("./cookies/{}.zhihu".format(cookie['name']), 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

    def parse(self, response):
        urls = response.css('div#SearchMain')
        pass