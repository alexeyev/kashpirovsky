# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
# from news_crawler.items import NewsItem
from pymongo import MongoClient
from scrapy.item import Item
 
 
class NewsSpider(CrawlSpider):
    name = "newsspider"
    allowed_domains = ["auto.newsru.ru"]
    start_urls = ["http://auto.newsru.ru/"]
    client = MongoClient()
    db = client['news_db']
    collection = db['news_collection']
 
    rules = (
    	Rule(SgmlLinkExtractor(allow=("\?page\=\d+"))),
    	Rule(SgmlLinkExtractor(allow=("\/article\/\d{2}\w{3}\d{4}\/\w+")), callback='parse_item'),
    )

    def parse_item(self, response):

		sel = Selector(response)
		#return item
		hxs = Selector(response)
		ex_item = 'Авто'.decode('utf-8')
		item_body = "".join(sel.xpath('//*[@id="text"]/p/text()').extract())

		#if (final_item_topic.find(ex_item) == -1):

		item = { "topic" : ex_item, 
				 "body" : item_body }


		self.collection.insert(item)

		#print hxs.xpath("//*[@id=\"root\"]/nav[2]/div/div/div[1]/div/a[@class=\"item dark active\"]/text()").extract()[0]

		#print i.extract()[0]

		#l.add_value('url', response.url)