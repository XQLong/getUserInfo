# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import pymysql
from twisted.enterprise import adbapi


class GetuserinfoPipeline(object):
    def __init__(self):
        # self.file = codecs.open('userinfo.json', 'a', encoding='utf-8')
        dbparms = dict(
            host='localhost',
            db='163music',
            user='root',
            passwd='1234',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,  # 指定 curosr 类型
            use_unicode=True,
        )
        # 指定擦做数据库的模块名和数据库参数参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    def process_item(self, item, spider):
        # print("pipline存储数据:"+ spider.name)
        # content = json.dumps(dict(item),ensure_ascii = False)+"\n"
        # self.file.write(content)
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        # cursor.execute(insert_sql, params)

    def close_spider(self, spider):
        self.file.close()
