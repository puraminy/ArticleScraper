# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
PAPER_MIN_YEAR = 2014

from scrapy.exceptions import DropItem

class FilterYearPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""
    def process_item(self, item, spider):
        global PAPER_MIN_YEAR
        proc_year = int(item['proc_year'])
        if proc_year < PAPER_MIN_YEAR:
            raise DropItem("Less than specified year : %s" % PAPER_MIN_YEAR)
        else:
            return item

class FilterMustContainsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    def process_item(self, item, spider):
        # mustContainWords = ['knowledge','rdf']
        mustContainWords = []
        find = False
        if len(mustContainWords) > 0:
            for word in mustContainWords:
                if item['paper_title'].lower().find(word) >= 0:
                    find = True
                    break
            if not find:
                raise DropItem("Not contain any of the specified words")
            else:
                return item
        else:
            return item

