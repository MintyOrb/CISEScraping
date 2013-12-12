from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from CISEScraping.items import CISEitem
import urlparse
from datetime import datetime, timedelta


class CISESpider(BaseSpider):
    handle_httpstatus_list = [404]
    name = 'JMUCISE'
    start_urls = [
        'http://www.cs.jmu.edu',
        'http://www.isat.jmu.edu',
        'http://www.cise.jmu.edu',
        'http://www.jmu.edu/engineering'
    ]

    EXCLUDE_FROM_ADDING = [
        ".zip", ".gif" , ".jpg" , ".jpeg" , ".doc" , ".ppt", ".pptx", ".avi" , ".pdf" , ".rtf", ".mov" , ".mp4" , ".xml" , ".dat" , ".nit" , 
        "google" , "facebook" , "digg" , "delicious" , ".sbx" , ".shp" , ".prj" , ".tgz" , "php?" , ".ps" , ".epx" , ".class" , ".dbf" ,
        "mailto:" , "javascript" , "@" , ".png" , ".sit" , ".shx" , ".sbn" , ".mdb" , ".ldb" , ".tif" , ".tfw" , ".aux" , ".atx" , ".rrd" ,
        ".dir" , ".001" , ".mp3" , ".eps" , ".xlsx" , ".swf"
    ]

    EXCLUDE_FROM_NO_DATE = [
        "users.cs.jmu" ,  "?"
    ]

    def parse(self, response):

        sel = Selector(response)

        CrawlItem = CISEitem()

    # get domain of response
        if "cs." in response.url:
            domain = 'Computer Science'
        if "engineering" in response.url:
            domain = 'Engineering'
        if "cise." in response.url:
            domain = 'CISE'
        if "isat." in response.url and "cisat." not in response.url:
            domain = 'ISAT'
        else:
            domain = 'other'

        if response.status == 200:

            if 'jmu.edu' in response.url and any(name in response.url.lower() for name in ('cs.' , 'engineering' , 'cise.' , 'isat.')):

            # scrape date and return item if page is old or there is no date

                if len(sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()) > 0:    
                   
                    lastUpdateStringList = sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()
                    today = datetime.today()

                    # get date in list (location in list differs from page to page)
                    for item in lastUpdateStringList:
                        if len(item) > 25 and len(item) < 45:
                            readableDate = item
                            
                    tempDate = readableDate.replace(":", " ").replace(",", " ")
                    # convert to python time obj
                    tempDate = datetime.strptime(tempDate, "%A %B %d %Y %I %M %p")
                    # add item if old
                    if today - tempDate > timedelta(days=90):
                        CrawlItem['group'] = "Old Page"
                        CrawlItem['domain'] = domain
                        CrawlItem["url"] = response.url
                        CrawlItem["lastUpdated"] = readableDate
                        CrawlItem["lastUpdatedDateTime"] = tempDate
                        yield CrawlItem

                elif not any(name in response.url for name in self.EXCLUDE_FROM_NO_DATE):
                    CrawlItem['group'] = "No Date On Page"
                    CrawlItem['domain'] = domain
                    CrawlItem['url'] = response.url
                    yield CrawlItem

            # get links from the page and yield new requests
                newLinks = []
                pageLinks = sel.xpath("//a/@href").extract()
                for link in pageLinks:
                    if "http://" not in link or "https://" not in link:
                        if not any(name in link.lower() for name in self.EXCLUDE_FROM_ADDING):
                            newLinks.append(urlparse.urljoin(response.url, link.strip()))
                    else:
                        newLinks.append(link)
                        
                for link in newLinks:   
                    yield Request(url=link, callback=self.parse)

        elif response.status == 404:
        # log broken link

            CrawlItem['group'] = "Page Not Found"
            CrawlItem['domain'] = domain
            CrawlItem['url'] = response.url
            CrawlItem['referrer'] = response.request.headers['Referer']

            yield CrawlItem
           
