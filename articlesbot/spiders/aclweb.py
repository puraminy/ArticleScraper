import scrapy
from articlesbot.items import PaperItem

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

        pub_item = PaperItem(pub_type='conf')

        for conf in confs_listing:
            pub_url = response.urljoin(conf.xpath('./@href').extract_first())
            pub_item['pub_name'] = conf.xpath('./text()').extract_first(),
            pub_item['pub_url'] = pub_url

            yield scrapy.Request(pub_url, callback=self.parse_proceedings,
                                 meta={'conf':  pub_item})

    def parse_proceedings(self, response):
        """
        Parse the list of proceedings here
        :param response:
        :return:
        """
        pub_item = response.meta.get('conf')
        listing_proceedings = response.xpath('//*[@id="main"]/div/div[contains(@class, "row")]')
        for proceedings in listing_proceedings:
           issue_year = proceedings.xpath('./div[1]/h4/a/text()').extract_first()
           proceedings_url = response.urljoin(proceedings.xpath('./div[2]/ul/li/a/@href').extract_first())
           issue_item =  pub_item.copy()
           issue_item['issue_name'] = proceedings.xpath('./div[2]/ul/li/a/text()').extract_first()
           issue_item['issue_url'] = proceedings_url
           issue_item['issue_year'] = issue_year
           yield scrapy.Request(proceedings_url, callback=self.parse_papers,
                                meta={'proc': issue_item})

    def parse_papers(self, response):
        """
        Parse the list of papers for each proceeding here
        :param response:
        :return:
        """
        issue_item = response.meta.get('proc')
        listing_papers = response.xpath('//*[@id="main"]/div[2]/p')
        for paper in listing_papers:
            paper_item = issue_item.copy()
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
        paper_abstract = response.xpath('string(//*[contains(@class, "acl-abstract")])').extract()
        paper_item['paper_abstract'] = paper_abstract
        paper_title = response.xpath('string(//h2[@id="title"])').extract()
        paper_item['paper_title'] = paper_title
        yield paper_item
