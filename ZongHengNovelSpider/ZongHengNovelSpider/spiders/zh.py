# -*- coding: utf-8 -*-
import scrapy
from ..items import ZonghengnovelspiderItem

class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ['zongheng.com']
    start_urls = ['http://book.zongheng.com/quanben/c0/c0/b9/u1/p1/v9/s1/t0/ALL.html']

    def parse(self, response):
        lis = response.xpath('//ul[@class="main_con"]/li')

        for li in lis:
            # 判断li标签class属性的值为空的话，表示该li包含了小说信息
            # print(li.xpath('@class').extract_first(''))
            if li.xpath('@class').extract_first('') == '':
                # 小说类型
                novel_type = li.xpath('span[@class="kind"]/a/text()').extract_first("不可知")
                novel_name = li.xpath('span/a[@class="fs14"]/text()').extract_first("")
                novel_clickNumber = li.xpath('span[@class="number"]/text()').extract_first("")
                # print('点击次数：',novel_clickNumber)
                # 去除点击次数中特殊字符
                # 在这里把转义字符全部替换为空字符串
                # \n换行 \r回车 \t横向制表符
                novel_clickNumber = novel_clickNumber.replace('\n','')
                novel_clickNumber = novel_clickNumber.replace('\r','')
                novel_clickNumber = novel_clickNumber.replace('\t', '')
                # print('点击次数：', novel_clickNumber)
                # 小说作者
                novel_author = li.xpath('span[@class="author"]/a/text()').extract_first("匿名")
                # 更新时间
                update_time = li.xpath('span[@class="time"]/text()').extract_first("已完结")
                update_time = update_time.replace('\n', '')
                update_time = update_time.replace('\r', '')
                update_time = update_time.replace('\t', '')

                item = ZonghengnovelspiderItem()
                item['novel_type'] = novel_type
                item['novel_name'] = novel_name
                item['novel_clickNumber'] = novel_clickNumber
                item['novel_author'] = novel_author
                item['update_time'] = update_time

                yield item