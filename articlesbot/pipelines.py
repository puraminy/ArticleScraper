# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
PAPER_MIN_YEAR = 2018

from scrapy.exceptions import DropItem


class ArticlesPipeline(object):
    def process_item(self, item, spider):
        return item

import json

class FilterYearPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""
    def process_item(self, item, spider):
        global PAPER_MIN_YEAR
        if item['proc_year'].lower():
            raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    def process_item(self, item, spider):
        if item['proc_year'].lower():
            raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
