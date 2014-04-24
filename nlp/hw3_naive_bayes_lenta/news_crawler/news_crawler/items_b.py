from scrapy.item import Item, Field
 
class NewsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title            = Field()
    name             = Field()
    url              = Field()