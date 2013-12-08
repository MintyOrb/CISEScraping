import json
from scrapy.mail import MailSender



class saveToFile(object):

    def __init__(self):
        # open files
    	self.old = open('old_pages.json', 'wb')
    	self.date = open('pages_without_dates.json', 'wb')
    	self.missing = open('missing_pages.json', 'wb')

        # write table headers
        line = "{0:10} {1:40} {2:} \n\n".format("Domain","Last Updated","URL")
        self.old.write(line)

        line = "{0:10} {1:} \n\n".format("Domain","URL")
        self.date.write(line)

        line = "{0:10} {1:70} {2:} \n\n".format("Domain","Page Containing Broken Link","URL of Broken Link")
        self.missing.write(line)
 

    def process_item(self, item, spider):
        
        if item['group'] == "Old Page":
            line = "{0:10} {1:40} {2:} \n".format(item['domain'],item["lastUpdated"],item["url"])
            self.old.write(line)
        elif item['group'] == "No Date On Page":
            line = "{0:10} {1:} \n".format(item['domain'],item["url"])
            self.date.write(line)
        elif item['group'] == "Page Not Found":
            line = "{0:10} {1:70} {2:} \n".format(item['domain'],item["referrer"],item["url"])
            self.missing.write(line)

        return item


        
# class emailResults(object):

#     def __init__(self):
#         mailer = MailSender()
#         dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
#         dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
    
#     def spider_opened(self, spider):
#         log.msg("opened spider  %s at time %s" % (spider.name,datetime.now().strftime('%H-%M-%S')))
    
#     def process_item(self, item, spider):
#             log.msg("Processsing item " + item['title'], level=log.DEBUG)
    
    
#     def spider_closed(JMUCISE):
#             mailer.send(to=["someone@example.com"], subject="Some subject", body="Some body", cc=["another@example.com"])
#         log.msg("closed spider %s at %s" % (spider.name,datetime.now().strftime('%H-%M-%S')))

# attachs (iterable) – an iterable of tuples (attach_name, mimetype, file_object) where attach_name is a string with the name that will appear on the e-mail’s attachment, mimetype is the mimetype of the attachment and file_object is a readable file object with the contents of the attachment

