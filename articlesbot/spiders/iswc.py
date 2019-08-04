import scrapy
import re
from data.scheme import DB_SCHEME

class ISWCSpider(scrapy.Spider):
    name = 'iswc'
    start_urls = [
        'https://link.springer.com/conference/semweb',
        'https://link.springer.com/conference/aswc'
    ]

    def parse(self, response):
        confs_listing = response.xpath('//*[contains(@id,"conference-list")]/div/ul[2]/li/a')
        conf_item = dict.fromkeys(DB_SCHEME)
        conf_item['conf_name'] = 'ISWC'
        conf_item['conf_url'] = 'https://link.springer.com/conference/semweb'
        for conf in confs_listing:
            proc_url = response.urljoin(conf.xpath('./@href').extract_first())
            proc_item = conf_item.copy()
            proc_item['proc_url'] = proc_url
            yield scrapy.Request(proc_url, callback=self.parse_papers,
                                 meta={'proc': proc_item})

    def parse_papers(self, response):
        """
        Parse the list of papers here
        :param response:
        :return:
        """
        proc_item = response.meta.get('proc')
        proc_name = response.xpath('//*[contains(@class,"conference-acronym")]/text()').extract_first()
        proc_item['proc_name'] = proc_name
        year_list = re.findall('\d+', proc_name)
        if len(year_list) > 0:
            proc_item['proc_year'] = year_list[0]
        listing_papers = response.xpath('//*/li[contains(@class,"chapter-item")]/div/div[1]/a')

        for paper in listing_papers:
            paper_item = proc_item.copy()
            paper_item['paper_title'] = paper.xpath('./text()').extract_first()
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
        paper_abstract = response.xpath('//*[@id="Abs1"]/p/text()').extract_first()
        paper_item['paper_abstract'] = paper_abstract
        paper_authors = response.xpath('//*[@id="authors"]/ul/descendant::*/text()')
        paper_item['paper_authors'] = paper_authors
        if paper_item:
            yield paper_item

# process = CrawlerProcess()
#process.crawl(ACLWebSpider)
# process.crawl(ISWCSpider)
# process.start() # the script will block here until all crawling jobs are finished