from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from CISEScraping.items import CISEDeadLinks, CISEOldPages, CISENoDate
import urlparse
from datetime import datetime, timedelta


class CISESpider(BaseSpider):
    name = 'JMUCISE'
    start_urls = [
        'http://www.cs.jmu.edu',
        'http://www.isat.jmu.edu',
        'http://www.cise.jmu.edu',
        'http://www.jmu.edu/engineering'
    ]

    def parse(self, response):

        sel = Selector(response)

        if response.status == 200:

            if 'jmu.edu' and ('cs' or 'engineering' or 'cise' or 'isat') in response.url:
                
            # scrape date and return item if page is old

                today = datetime.today()

                if len(sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()) > 0:
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
                else:
                    noDate = CISENoDate()
                    noDate['url'] = response.url
                    yield noDate


            # get links from the page and yield new requests
                newLinks = []
                pageLinks = sel.xpath("//a/@href").extract()
                for link in pageLinks:
                    if "http://" or "https://" not in link:
                        if "mail" not in link and "pdf" not in link and "rtf" not in link and "javascript" not in link:
                            newLinks.append(urlparse.urljoin(response.url, link.strip()))
                        
                
                for link in newLinks:   
                    print link
                    yield Request(url=link, callback=self.parse)


        else:
            # log broken links
            deadLinks = CISEDeadLinks()

            deadLinks['deadLinkURL'] = response.url
            deadLinks['referrer'] = response.referer
            deadLinks['HTTPStatus'] = response.status

            yield deadLinks

            # issues to work out
        # jmu.edu and 'cs' or 'eng' etc - why only true when in included is first after and?
        # look into item pipeline for sorting items? Write to seperate files 

        # div id="pagecontent" h1 title - find internal 404s
        # last updated list - get date every time - use length?
        # functional refactor (less prodecural)
        # add days since update?

        # potential functions:
            # addDeadLink
            # addOldPage
            # addNoDate
            # getNewLinks



