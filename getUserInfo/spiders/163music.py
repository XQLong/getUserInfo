import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from getUserInfo.items import UserInfo
import logging

class userinfoSpider(scrapy.Spider):

    name = '163musicuser'
    allowed_domains = ["163.com"]
    base_url = "https://music.163.com/#/user/home?id="


    def start_requests(self):
        self.log('okoko')
        i = 1000
        while i<1100:
            url = self.base_url + str(i)
            yield Request(url = url, callback=self.parse, meta={'page': '用户首页'}, dont_filter=True)
            i+=1

    def parse(self, response):
        sta = response.xpath("//div[contains(@class,'n-for404')]").extract()
        if len(sta) == 0:
            user = ItemLoader(item=UserInfo(), response=response)
            idlink = response.xpath("//ul/li/a[contains(@href,'/user/event?id')]/@href").extract()
            if idlink:
                id = idlink[0].split('=')[-1]
            else:
                self.crawler.engine.close_spider(self, 'response msg error %s, job done!' % response.text)
            nickname = response.xpath(
                "//div[contains(@class,'name')]/div/h2[contains(@id,'j-name-wrap')]/span[contains(@class,'tit')]/text()").extract()
            events = response.xpath("//ul/li/a/strong[contains(@id,'event_count')]/text()").extract()
            folowers = response.xpath("//ul/li/a/strong[contains(@id,'follow_count')]/text()").extract()
            fans = response.xpath("//ul/li/a/strong[contains(@id,'fan_count')]/text()").extract()
            user.add_value('userid', id)
            user.add_value('nickname', nickname)
            user.add_value('events', events)
            user.add_value('folowers', folowers)
            user.add_value('fans', fans)
            return user.load_item()
