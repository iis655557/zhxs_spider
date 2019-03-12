# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os
import xlwt
import sqlite3

class ZonghengnovelspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JSONWriterPipeline(object):
    def __init__(self):
        # 做写入数据前的准备工作
        self.file = codecs.open('zongheng.json', 'w+', encoding='utf-8')
        # 先写入一个左中括号
        self.file.write('[')
        # [{},{},{},{},
    def process_item(self, item, spider):
        # 先把item转为字典类型
        item = dict(item)
        # 把字典转为json字符串
        json_str = json.dumps(item) + ','
        # 将字符串写入文件
        self.file.write(json_str)

        return item

    def close_spider(self,spider):
        self.file.seek(-1,os.SEEK_END)
        self.file.truncate()
        self.file.write(']')
        self.file.close()

class ExcelWriterPipeline(object):
    def __init__(self):
        # 创建工作薄
        self.workbook = xlwt.Workbook(encoding='utf-8')
        # 添加sheet表
        self.sheet = self.workbook.add_sheet('纵横小说网')
        # 写入表头
        self.sheet.write(0, 0, 'novel_name')
        self.sheet.write(0, 1, 'novel_type')
        self.sheet.write(0, 2, 'novel_author')
        self.sheet.write(0, 3, 'novel_clickNumber')
        self.sheet.write(0, 4, 'update_time')
        # 记录行号
        self.count = 1

    def process_item(self, item, spider):
        self.sheet.write(self.count, 0, item['novel_name'])
        self.sheet.write(self.count, 1, item['novel_type'])
        self.sheet.write(self.count, 2, item['novel_author'])
        self.sheet.write(self.count, 3, item['novel_clickNumber'])
        self.sheet.write(self.count, 4, item['update_time'])

        self.count += 1

        return item
    def close_spider(self,spider):
        self.workbook.save('zongheng.xls')

class SQLWriterPipeline(object):
    def __init__(self):
        self.connect = sqlite3.connect('zongheng.db')
        self.cursor = self.connect.cursor()

        try:
            sql = 'create table novel (id integer primary key, novel_name text, novel_type text, novel_author text, novel_clickNumber text, update_time text)'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        sql = 'insert into novel (novel_name,novel_type,novel_author,novel_clickNumber,update_time) values ("%s","%s","%s","%s","%s")'%(item['novel_name'],item['novel_type'],item['novel_author'],item['novel_clickNumber'],item['update_time'])
        self.cursor.execute(sql)

        self.connect.commit()

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()