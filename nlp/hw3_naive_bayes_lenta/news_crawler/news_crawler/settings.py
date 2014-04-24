# Scrapy settings for news_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_crawler (+http://www.yourdomain.com)'
