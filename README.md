# ArticleScraper
A web scraper based on Scrapy to harvest scientific papers from conference and journal websites. To get familiar with Scrapy, please vist the website https://docs.scrapy.org/en/latest/ 

# Database scheme

We gather the following information about each article:

```python
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
    paper_pdf = scrapy.Field() # The url to the pdf file of the paper if available
    paper_poster = scrapy.Field() # The poster file to the video of the paper if available
    paper_video = scrapy.Field() # The url to the video of the paper if available
    pass
```



# Creating a new spider

The spiders are kept in the `spiders` folder. There are currently two spiders, `aclweb` and `iswc`, in this folder. Each spider is defined as a class in one or seperated files. You can use them as example. For more information about spiders, refer to https://docs.scrapy.org/en/latest/topics/spiders.html

The `aclweb` spider gathers the papers from the ACL website: https://www.aclweb.org/anthology/. This URL is defined in the `start_urls`. Please note that the name of the spider is also defined in the class. This name is later used to run the spider.


```python
class ACLWebSpider(scrapy.Spider):
    """ A spider to collect articles from ACLWeb.org website """
    name = 'aclweb'
    start_urls = [
        'https://www.aclweb.org/anthology/',
    ]
    def parse(self, response):
    ...
```


# Running a spider

To run a spider use a command line in the Terminal of python. 

`scrapy crawl aclweb -o papers.csv` 

# Logging

If you want to store the output of the Scrapy run to a log file, you can specify the log file name in settings

`LOG_FILE = mylog.log`

For more information about logging check https://docs.scrapy.org/en/latest/topics/logging.html

There are command-line arguments, available for all commands, that you can use to override some of the Scrapy settings regarding logging.

`--logfile FILE
Overrides LOG_FILE
`
