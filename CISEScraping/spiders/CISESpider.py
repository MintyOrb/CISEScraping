from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from CISEScraping.items import CISEitem
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

            if 'jmu.edu' in response.url and any(name in response.url for name in ('cs' , 'engineering' , 'cise' , 'isat')):
                
            # scrape date and return item if page is old

                today = datetime.today()

                if len(sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()) > 0:    
                    lastUpdateStringList = sel.xpath("//div[@id='footer']/child::p[position()=1]/text()").extract()
                    tempDate = ""
                    for item in lastUpdateStringList:
                        if len(lastUpdateStringList) > len(tempDate):
                            tempDate = item

                    tempDate = tempDate.replace(":", " ").replace(",", " ")
                    # convert to python time obj
                    lastUpdateTime = datetime.strptime(tempDate, "%A %B %d %Y %I %M %p")
                    # add item if old
                    if today - lastUpdateTime > timedelta(days=30):
                        oldPage = CISEitem()
    
                        oldPage["url"] = response.url
                        oldPage["lastUpdated"] = lastUpdateStringList[1]
                        print oldPage
                        return oldPage
                else:
                    noDate = CISEitem()
                    noDate['url'] = response.url
                    return noDate


            # get links from the page and return new requests
                newLinks = []
                pageLinks = sel.xpath("//a/@href").extract()
                for link in pageLinks:
                    if "http://" not in link or "https://" not in link:
                        if not any(name in link for name in ("mail" , "pdf" , "rtf" , "javascript")):
                            newLinks.append(urlparse.urljoin(response.url, link.strip()))
                    else:
                        newLinks.append(link)
                        
                
                for link in newLinks:   
                    print link
                    return Request(url=link, callback=self.parse)


        else:
        # log broken link
            deadLinks = CISEitem()

            deadLinks['url'] = response.url
            deadLinks['referrer'] = response.referer
            deadLinks['HTTPStatus'] = response.status

            return deadLinks



