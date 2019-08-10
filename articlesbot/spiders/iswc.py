import scrapy
import re
from articlesbot.items import PaperItem

class ISWCSpider(scrapy.Spider):
    name = 'iswc'
    start_urls = [
        'https://link.springer.com/conference/semweb',
        'https://link.springer.com/conference/aswc'
    ]

    def parse(self, response):
        confs_listing = response.xpath('//*[contains(@id,"conference-list")]/div/ul[2]/li/a')
        pub_item = PaperItem(pub_type='conf')
        pub_item['pub_name'] = 'ISWC'
        pub_item['pub_url'] = 'https://link.springer.com/conference/semweb'
        for conf in confs_listing:
            issue_url = response.urljoin(conf.xpath('./@href').extract_first())
            issue_item =  pub_item.copy()
            issue_item['issue_url'] =  issue_url
            yield scrapy.Request( issue_url, callback=self.parse_papers,
                                 meta={'proc':  issue_item})

    def parse_papers(self, response):
        """
        Parse the list of papers here
        :param response:
        :return:
        """
        issue_item = response.meta.get('proc')
        issue_name = response.xpath('//*[contains(@class,"conference-acronym")]/text()').extract_first()
        issue_item['issue_name'] = issue_name
        year_list = re.findall('\d+', issue_name)
        if len(year_list) > 0:
            issue_item['issue_year'] = year_list[0]
        listing_papers = response.xpath('//*/li[contains(@class,"chapter-item")]/div/div[1]/a')

        for paper in listing_papers:
            paper_item = issue_item.copy()
            paper_url = response.urljoin(paper.xpath('./@href').extract_first())
            paper_item['paper_url'] = paper_url
            yield scrapy.Request(paper_url, callback=self.parse_paper_details,
                                 meta={'paper': paper_item})

    def parse_paper_details(self, response):
        """
        Parse the paper page here
        :param response:
        :return:
        """
        paper_item = response.meta.get('paper')
        paper_item['paper_title'] = response.xpath('string(//*[contains(@class, "ChapterTitle")])').extract()
        paper_abstract = response.xpath('string(//*[@id="Abs1"]/p)').extract()
        paper_item['paper_abstract'] = paper_abstract
        paper_authors = response.xpath('string(//*[@id="authors"])').extract()
        paper_item['paper_authors'] = paper_authors
        if paper_item:
            yield paper_item

