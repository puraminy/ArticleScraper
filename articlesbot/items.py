# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    pub_type = scrapy.Field() # values: conf, journal
    pub_name = scrapy.Field() # the name of the conference of journal
    pub_url = scrapy.Field()
    issue_name = scrapy.Field()
    issue_url = scrapy.Field()
    issue_year = scrapy.Field()
    paper_title = scrapy.Field() 
    paper_url = scrapy.Field() 
    paper_abstract = scrapy.Field() 
    paper_keywords = scrapy.Field() 
    paper_doi = scrapy.Field()
    paper_authors = scrapy.Field()
    paper_pdf = scrapy.Field()
    paper_poster = scrapy.Field()
    paper_video = scrapy.Field()
    pass
