from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from CISEScraping.items import CISEDeadLinks, CISEOldPages
import urlparse
from datetime import datetime, timedelta


class CISESpider(BaseSpider):
    name = 'JMUCISE'
    start_urls = [
        'http://www.cs.jmu.edu',
        # 'http://www.isat.jmu.edu',
        # 'http://www.cise.jmu.edu',
        # 'http://www.jmu.edu/engineering'
    ]

    def parse(self, response):

        sel = Selector(response)

        if response.status == 200:

            print "Hello!"

            if 'jmu.edu' and ('cs' or 'engineering' or 'cise' or 'isat') in response.url:

                print "Inside if!"
                
            # scrape date and return item if page is old

                today = datetime.today()

                lastUpdateStringList = sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()
                tempDate = lastUpdateStringList[1].replace(":", " ").replace(",", " ")
                # convert to python time obj
                lastUpdateTime = datetime.strptime(tempDate, "%A %B %d %Y %I %M %p")
                # add item if old
                if today - lastUpdateTime > timedelta(days=30):
                    oldPage = CISEOldPages()

                    oldPage["url"] = response.url
                    oldPage["lastUpdated"] = lastUpdateStringList[1]
                    
                    yield oldPage  

            # get links from the page and yield new requests
                newLinks = []
                pageLinks = sel.xpath("//a/@href").extract()
                for link in pageLinks:
                    if "http://" and "mail" and "pdf" and "rtf" not in link:
                        newLinks.append(urlparse.urljoin(response.url, link.strip()))
                    # elif  not in link:
                    #     newLinks.append(urlparse.urljoin(response.url, link.strip()))
                
                for link in newLinks:   
                    print link
                    yield Request(url=link, callback=self.parse)


        else:
            # log broken links
            deadLinks = CISEDeadLinks()

            deadLinks['deadLinkURL'] = response.url
            deadLinks['referrer'] = request.referer

            return deadLinks



