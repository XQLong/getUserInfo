# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from getUserInfo.settings import USER_AGENT_LIST


class JsPageSpiderMiddleware(object):
    def __init__(self):
        option = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        # option.add_experimental_option("excludeSwitchs",["ignore-certificate-errors"])
        # 不加载图片
        option.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(executable_path="E:\stu\Machine_Learning\Python_Ecosystem\chromedriver.exe",chrome_options=option)
        super(JsPageSpiderMiddleware, self).__init__()

    def process_request(self,request,spider):
        if spider.name == "163musicuser":
            # browser = webdriver.Chrome(executable_path="E:\stu\Machine_Learning\Python_Ecosystem\chromedriver.exe")
            browser = self.browser
            browser.get(request.url)
            browser.implicitly_wait(10)
            # time.sleep(2)
            try:
                browser.switch_to.frame("contentFrame")
            except:
                self.crawler.engine.close_spider(spider,'出现异常')
                pass
            # blist = browser.find_element_by_tag_name('b')
            # print("个数".format(len(blist)))
            print("访问{0}".format(request.url))
            return HtmlResponse(url=browser.current_url,body=browser.page_source,encoding="utf-8")

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class MyproxyMiddleware(object):
    """docstring for ProxyMiddleWare"""

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        # proxy = self.get_random_proxy()
        haha = random.randint(0,10)
        if haha >= 5:
            print('\n随机{}正在使用代理\n'.format(haha))
            proxy = 'http://127.0.0.1:8087'
            request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = 'http://127.0.0.1:8087'
            # print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        proxy = 'http://127.0.0.1:8087'
        request.meta['proxy'] = proxy
        return request

class GetuserinfoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class GetuserinfoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
