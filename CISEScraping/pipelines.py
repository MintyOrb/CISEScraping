from scrapy.mail import MailSender
from datetime import datetime
from scrapy.signals import spider_closed, spider_opened

class saveToFile(object):

    def __init__(self):
        # open files
    	self.old = open('old_pages.txt', 'wb')
    	self.date = open('pages_without_dates.txt', 'wb')
    	self.missing = open('missing_pages.txt', 'wb')

        # write table headers
        line = "{0:15} {1:40} {2:} \n\n".format("Domain","Last Updated","URL")
        self.old.write(line)

        line = "{0:15} {1:} \n\n".format("Domain","URL")
        self.date.write(line)

        line = "{0:15} {1:70} {2:} \n\n".format("Domain","Page Containing Broken Link","URL of Broken Link")
        self.missing.write(line)

    def process_item(self, item, spider):
        
        # add items to file as they are scraped
        if item['group'] == "Old Page":
            line = "{0:15} {1:40} {2:} \n".format(item['domain'],item["lastUpdated"],item["url"])
            self.old.write(line)
        elif item['group'] == "No Date On Page":
            line = "{0:15} {1:} \n".format(item['domain'],item["url"])
            self.date.write(line)
        elif item['group'] == "Page Not Found":
            line = "{0:15} {1:70} {2:} \n".format(item['domain'],item["referrer"],item["url"])
            self.missing.write(line)

        return item

class twentyOldest(object):

    def __init__(self):

        #dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

        # open file
        self.oldOutput = open('twenty_oldest_pages.txt', 'wb')

        # write table header
        line = "{0:15} {1:40} {2:} \n\n".format("Domain","Last Updated","URL")

        # create dict for storing oldest pages
        self.oldest = {'lastUpdatedDateTime':0}

    def process_item(self, item, spider):
        
        if item['group'] == "Old Page":
            # get list of dates from list of oldest pages 
            listOfValues = [x['lastUpdatedDateTime'] for x in self.oldest]
            # id item is older than youngest item in the dict, remove that item and add the new one
            if item['lastUpdatedDateTime'] < min(listOfValues):
                if len(self.oldest) > 20:
                    # delete current 'youngest'
                    place = self.oldest.index(min(self.oldest))
                    del self.oldest[place]
                # add new item
                self.oldest.append(item)

        return item

    def spider_closed(JMUCISE):

        # sort the array based on age
        self.oldest = sorted(self.oldest, key=lambda k: k['lastUpdatedDateTime']) 

        # write the dict to the file created
        for item in oldest:
            line = "{0:15} {1:40} {2:} \n".format(item['domain'],item["lastUpdated"],item["url"])
            self.oldOutput.write(line)

        return item

        