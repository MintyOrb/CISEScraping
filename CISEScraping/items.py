# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CISEDeadLinks(Item):
    deadLinkURL = Field()
    referrer = Field()
    HTTPStatus = Field()

class CISEOldPages(Item):
    url = Field()
    lastUpdated = Field()

class CISENoDate(Item):
    url = Field()

    
#make a single item?
# class UtilityItem(Item):
# 	group = Field()
#     url = Field()
#     referrer = Field()
#     HTTPStatus = Field()
#     lastUpdated = Field()
#     # daysSinceUpdated = Field()
