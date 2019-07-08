# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfo(scrapy.Item):
    # define the fields for your item here like:
    userid = scrapy.Field()
    nickname = scrapy.Field()
    events = scrapy.Field()
    folowers = scrapy.Field()
    fans = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                   INSERT INTO userinfo(num,userid,nickname,events,followers,fans)
                    VALUES (NULL,%s, %s, %s, %s,%s);
               """
        params = (self["userid"][0], self["nickname"][0], self["events"][0], self["folowers"][0],self["fans"][0],)
        # print(insert_sql + str(params))
        return insert_sql, params
    pass
