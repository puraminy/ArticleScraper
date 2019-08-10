# ArticleScraper
A web scraper based on Scrapy to harvest scientific papers from conference and journal websites. You need to install `scrapy` package for your python IDE. To get familiar with Scrapy, please vist the website https://docs.scrapy.org/en/latest/ 

# Database scheme

We gather the following information about each article. This class is in the `items.py` file. This is the common scheme for all spider to gather consistent information.

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

The items are stored in a `csv` file. Currently, the gathered articles are in `data/papers.csv`.

# Creating a new spider

The spiders are kept in the `spiders` folder. There are currently two spiders, `aclweb` and `iswc`, in this folder. Each spider is defined as a class in one or seperated files. We recommand to use a separate file for each spider. For more information about spiders, refer to https://docs.scrapy.org/en/latest/topics/spiders.html

As an example, the `aclweb` spider gathers the papers from the ACL website: https://www.aclweb.org/anthology/. This URL is defined in the `start_urls` of the class. Please note that the name of the spider is also defined in the class. This name is later used to run the spider. You can use this spider as an example to develope new spiders for other websites. 


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

`scrapy crawl aclweb -o data/papers.csv` 

The gattered items by the spider will be appended to the `data/papers.csv`.

# Filtering items

If you want to filter the scraped items based on some fileds you can use the `pipelines`. Papelines are used for post-procssing the fetched itmes. We currently implemented two filters to filter the items based on the publishing year and some words in the title. However, we don't recommend to use these filters at this stage. These filters can be later applied on the database.

To activate a pipeline, you need to add it to the `ITEM_PIPELINES` in the settings file:

```
ITEM_PIPELINES = {
    # 'articlesbot.pipelines.FilterYearPipeline': 1,
    # 'articlesbot.pipelines.FilterMustContainsPipeline': 2,
    # 'articlesbot.pipelines.JsonWriterPipeline': 3
}
```

For more information on pipelines please refer to: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Logging

If you want to store the output of the Scrapy run to a log file, you can specify the log file name in the settings:

`LOG_FILE = mylog.log`

or use the `--logfile` opetion when running a spider:

`scrapy crawl aclweb -o papers.csv --logfile mylog.log`

The output of Scrapy contains warning, info or errors of the running spider. So, the logfile can be useful to check the possible errors.

# Generating reports and statistics

You can generate reports based on the databasae by writing custom functions. We already wrote `generate.py` which generate an html file contianing the title, year and the abstract of some selected papers. You can also use applications like Excel, SPSS or R to process the database. `TAD` viewer is a simple tool to view and filter the database: https://www.tadviewer.com/. We recommend R to process and generatign reports on the articles.

You can pull intersting reports to `reports` folder.

#  Collaboration

If you want to colloberate on the project, you can clone the `nlplab` branch using `git` and then push the changes to this branch. Later, using pull requests changes will be merged to the `master` branch. To get started on using `github` please refer to: https://guides.github.com/activities/hello-world/


