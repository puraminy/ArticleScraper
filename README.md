# ArticleScraper
A web scraper based on scrapy to harvest scientific papers from conferences and journal websites.

# Database scheme

We gather the following information about each article:

`DB_SCHEME = ['conf_name', 'conf_url',
                    'proc_name', 'proc_url', 'proc_year',
                    'paper_title', 'paper_url', 'paper_abstract', 'paper_keywords', 'paper_doi',
                    'paper_authors',
                    'paper_pdf_url','paper_poster_url', 'paper_video_url']`



# Creating a new spider

The spiders are 

# Run an spider

`scrapy crawl name_of_spider - results.csv` 

# Logging

If you want to store the output of the Scrapy run to a log file, you can specify the log file name in settings

`LOG_FILE = mylog.log`

For more information about logging check https://docs.scrapy.org/en/latest/topics/logging.html

There are command-line arguments, available for all commands, that you can use to override some of the Scrapy settings regarding logging.

`--logfile FILE
Overrides LOG_FILE
`
