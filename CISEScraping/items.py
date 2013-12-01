# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CISEDeadLinks(Item):
    deadLinkURL = Field()
    referrer = Field()

class CISEOldPages(Item):
    URL = Field()
    lastUpdated = Field()
    
