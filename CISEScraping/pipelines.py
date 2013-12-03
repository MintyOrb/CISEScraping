# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# class CISEscrapingPipeline(object):
#     def process_item(self, item, spider):
#         return item

import json

class saveToFile(object):

    def __init__(self):
    	self.old = open('old_pages', 'wb')
    	self.date = open('pages_without_dates.json', 'wb')
    	self.missing = open('missing_pages.json', 'wb')
 

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        
        if item['group'] == "Old Page":
        	self.old.write(line)
        elif item['group'] == "No Date On Page":
        	self.date.write(line)
        elif item['group'] == "Page Not Found":
        	self.missing.write(line)

        return item
