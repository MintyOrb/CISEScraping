from scrapy.mail import MailSender
from datetime import datetime
from scrapy.signals import spider_closed, spider_opened
from scrapy.xlib.pydispatch import dispatcher

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

class emailResults(object):

    def __init__(self):

        dispatcher.connect(self.spider_closed, spider_closed)
        dispatcher.connect(self.spider_opened, spider_opened)

        old = open('old_pages.txt', 'wb')
        date = open('pages_without_dates.txt', 'wb')
        missing = open('missing_pages.txt', 'wb')
        oldOutput = open('twenty_oldest_pages.txt', 'wb')
       
        self.mailer = MailSender()

    def spider_closed(JMUCISE):

        self.mailer.send(to=["bornytm@gmail.com"], attachs=attachments, subject="test email", body="Some body")

        self.mailer.send(to=["radochlm@jmu.edu"], attachs=attachments, subject="CISE Site Crawling Spider Delivery", body="Some body", cc=["bornytm@gmail.com"])
    
    # for testing purposes

    def spider_opened(JMUCISE):
        for x in range(100):
            print "opened"
        attachments = [
            ("old_pages", "text/plain", old)
            ("date", "text/plain", date)
            ("missing", "text/plain", missing)
            ("oldOutput", "text/plain", oldOutput)
        ]
        mailer = MailSender()
        mailer.send(to=["bornytm@gmail.com"], attachs=attachments, subject="test email", body="Some body")


class twentyOldest(object):

    # create list for storing oldest pages dics and values in item
    oldest = [{'lastUpdatedDateTime':datetime.today()}]

    #open file
    oldOutput = open('twenty_oldest_pages.txt', 'wb')

    def __init__(self):

        dispatcher.connect(self.spider_closed, spider_closed)

        # open file
        # self.oldOutput = open('twenty_oldest_pages.txt', 'wb')

        # write table header
        line = "{0:15} {1:40} {2:} \n\n".format("Domain","Last Updated","URL")
        self.oldOutput.write(line)

    def process_item(self, item, spider):
        
        if item['group'] == "Old Page":
            itemAge = item['lastUpdatedDateTime']
     
            currentYoungest = max(x['lastUpdatedDateTime'] for x in self.oldest)

            # if item is older than youngest item in the list, remove that item (if list has more than 20 pages) and add the new one
            if itemAge < currentYoungest:
                if len(self.oldest) > 20:
                    # delete current 'youngest'
                    place = self.oldest.index(max(self.oldest, key=lambda x:x['lastUpdatedDateTime']))
                    del self.oldest[place]

                # add new item
                self.oldest.append(item)
                

        return item

    def spider_closed(JMUCISE):

        # sort the array based on age
        oldest = sorted(oldest, key=lambda k: k['lastUpdatedDateTime']) 

        # write the dict to the file created
        for item in oldest:
            line = "{0:15} {1:40} {2:} \n".format(item['domain'],item["lastUpdated"],item["url"])
            oldOutput.write(line)

        return item
