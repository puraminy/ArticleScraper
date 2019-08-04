import scrapy
from scrapy.crawler import CrawlerProcess

ArticleBase_Keys = ['conf_name', 'conf_url',
                    'proc_name', 'proc_url', 'proc_year',
                    'paper_title', 'paper_url', 'paper_abstract', 'paper_keywords', 'paper_doi',
                    'paper_authors',
                    'paper_pdf_url','paper_poster_url', 'paper_video_url']

class ACLWebSpider(scrapy.Spider):
    name = 'aclweb'
    start_urls = [
        'https://www.aclweb.org/anthology/',
    ]
    def parse(self, response):
        ACL_events = '//*[@id="main-container"]/div/div[2]/main/table[1]/tbody/tr[1]/th/a'
        NON_ACL_events = '//*[@id="main-container"]/div/div[2]/main/table[2]/tbody/tr[1]/th/a'
        acl_confs_listing = response.xpath(ACL_events)
        nonacl_confs_listing = response.xpath(NON_ACL_events)
        confs_listing = acl_confs_listing + nonacl_confs_listing

        global ArticleBase_Keys
        conf_item = dict.fromkeys(ArticleBase_Keys)

        for conf in confs_listing:
            conf_url = response.urljoin(conf.xpath('./@href').extract_first())
            conf_item['conf_name'] = conf.xpath('./text()').extract_first(),
            conf_item['conf_url'] = conf_url

            yield scrapy.Request(conf_url, callback=self.parse_proceedings,
                                 meta={'conf': conf_item})

    def parse_proceedings(self, response):
        """
        Parse the listing page urls here
        :param response:
        :return:
        """
        conf_item = response.meta.get('conf')
        listing_proceedings = response.xpath('//*[@id="main"]/div/div[contains(@class, "row")]')
        for proceedings in listing_proceedings:
            proc_year = proceedings.xpath('./div[1]/h4/a/text()').extract_first()
            proceedings_url = response.urljoin(proceedings.xpath('./div[2]/ul/li/a/@href').extract_first())
            proc_item = conf_item.copy()
            proc_item['proc_name'] = proceedings.xpath('./div[2]/ul/li/a/text()').extract_first()
            proc_item['proc_url'] = proceedings_url
            proc_item['proc_year'] = proc_year
            yield scrapy.Request(proceedings_url, callback=self.parse_papers,
                                 meta={'proc': proc_item})

    def parse_papers(self, response):
        """
        Parse paper here
        :param response:
        :return:
        """
        proc_item = response.meta.get('proc')

        listing_papers = response.xpath('//*[@id="main"]/div[2]/p')

        for paper in listing_papers:
            paper_item = proc_item.copy()
            paper_item['paper_pdf'] = response.urljoin(paper.xpath('./span[1]/a/@href').extract_first())
            paper_item['paper_title'] = paper.xpath('./span[2]/strong/a/text()').extract_first()
            paper_url = response.urljoin(paper.xpath('./span[2]/strong/a/@href').extract_first())
            paper_item['paper_url'] = paper_url
            yield scrapy.Request(paper_url, callback=self.parse_paper_details,
                                 meta={'paper': paper_item})

    def parse_paper_details(self, response):
        """
        Parse paper details here
        :param response:
        :return:
        """
        paper_item = response.meta.get('paper')
        paper_abstract = response.xpath('//*[contains(@class, "acl-abstract")]/text()').extract_first()
        paper_item['paper_abstract'] = paper_abstract
        yield paper_item

class ISWCSpider(scrapy.Spider):
    name = 'iswc'
    start_urls = [
        'https://link.springer.com/conference/semweb',
        'https://link.springer.com/conference/aswc'
    ]

    def parse(self, response):
        confs_listing = response.xpath('//*[contains(@id,"conference-list")]/div/ul[2]/li/a')
        global ArticleBase_Keys
        conf_item = dict.fromkeys(ArticleBase_Keys)
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
        Parse paper here
        :param response:
        :return:
        """
        proc_item = response.meta.get('proc')
        proc_name = response.xpath('//*[contains(@class,"conference-acronym")]/text()').extract_first()
        proc_item['proc_name'] = proc_name
        year_list = [int(s) for s in proc_name.split() if s.isdigit()]
        if len(year_list):
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
        Parse paper details here
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