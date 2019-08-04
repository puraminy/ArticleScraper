import scrapy
from data.scheme import DB_SCHEME

class ACLWebSpider(scrapy.Spider):
    """ A spider to collect articles from ACLWeb.org website """
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

        conf_item = dict.fromkeys(DB_SCHEME)

        for conf in confs_listing:
            conf_url = response.urljoin(conf.xpath('./@href').extract_first())
            conf_item['conf_name'] = conf.xpath('./text()').extract_first(),
            conf_item['conf_url'] = conf_url

            yield scrapy.Request(conf_url, callback=self.parse_proceedings,
                                 meta={'conf': conf_item})

    def parse_proceedings(self, response):
        """
        Parse the list of proceedings here
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
        Parse the list of papers for each proceeding here
        :param response:
        :return:
        """
        proc_item = response.meta.get('proc')

        listing_papers = response.xpath('//*[@id="main"]/div[2]/p')

        for paper in listing_papers:
            paper_item = proc_item.copy()
            paper_item['paper_pdf'] = response.urljoin(paper.xpath('./span[1]/a/@href').extract_first())
            paper_url = response.urljoin(paper.xpath('./span[2]/strong/a/@href').extract_first())
            paper_item['paper_url'] = paper_url
            yield scrapy.Request(paper_url, callback=self.parse_paper_details,
                                 meta={'paper': paper_item})

    def parse_paper_details(self, response):
        """
        Parse paper page here
        :param response:
        :return:
        """
        paper_item = response.meta.get('paper')
        paper_abstract = response.xpath('//*[contains(@class, "acl-abstract")]/text()').extract_first()
        paper_item['paper_abstract'] = paper_abstract
        paper_title = response.xpath('//*[@id="title"]/a/text()')
        paper_item['paper_title'] = paper_title
        yield paper_item
