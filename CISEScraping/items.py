from scrapy.item import Item, Field

class CISEitem(Item):
	group = Field()
	url = Field()
	referrer = Field()
	lastUpdated = Field()
	domain = Field()

