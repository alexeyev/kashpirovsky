# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from news_crawler.items import NewsItem
from pymongo import MongoClient
from scrapy.item import Item
 
 
class NewsSpider(CrawlSpider):
    name = "newsspider"
    allowed_domains = ["lenta.ru"]
    start_urls = ["http://lenta.ru/2014/01/01/"]
    client = MongoClient()
    db = client['news_db']
    collection = db['news_collection']
 
    rules = (
    	Rule(SgmlLinkExtractor(allow=("\/\d{4}\/\d{2}\/\d{2}\/$"))),
    	Rule(SgmlLinkExtractor(allow=("\/\d{4}\/\d{2}\/\d{2}\/\w+")), callback='parse_item'),
    )

    def parse_item(self, response):

    	#sel = Selector(response)
        #return item
	    hxs = Selector(response)
	    #l = NewsLoader(NewsItem(), hxs)
	    item_title = hxs.xpath('//*[@id=\"root\"]/nav[2]/div/div/div[1]/div/a[@class=\"item dark active\"]/text()').extract() #.encode('utf-8')

	    if (len(item_title) > 0):

		final_item_topic = item_title[0].strip()
		item_body = "".join(hxs.xpath("//*[@id=\"root\"]/div[2]/div/div[1]/div[1]/div/div/div[@itemprop=\"articleBody\"]/p/text()").extract())

		ex_item = 'Все'.decode('utf-8')

		if (final_item_topic.find(ex_item) == -1):

		    item = { "topic" : final_item_topic, 
		    		 "body" : item_body }


		    self.collection.insert(item)

	    

	    #print hxs.xpath("//*[@id=\"root\"]/nav[2]/div/div/div[1]/div/a[@class=\"item dark active\"]/text()").extract()[0]

	    #print i.extract()[0]

	    #l.add_value('url', response.url)
