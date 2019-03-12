# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZonghengnovelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    novel_type = scrapy.Field()
    novel_name = scrapy.Field()
    novel_clickNumber = scrapy.Field()
    novel_author = scrapy.Field()
    update_time = scrapy.Field()

