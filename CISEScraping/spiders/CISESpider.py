from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.item import CISEDeadLinks, CISEOldPages
import urlparse
import datetime


class CISESpider(CrawlSpider):
    name = 'JMUCISE'
    start_urls = [
        'http://www.cs.jmu.edu',
        'http://www.isat.jmu.edu',
        'http://www.cise.jmu.edu',
        'http://www.jmu.edu/engineering'
    ]

    #follow all links (no restrictions on domain) and parse
    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_response'),
    )

    def parse_response(self, response):

        sel = HtmlXPathSelector(response)

        if response.status == 200:


            if 'jmu.edu' and ('cise' or 'engineering' or 'cs' or 'isat') in response.url:
                
            # scrape date and return item if page is old

                today = datetime.today()

                lastUpdateStringList = sel.Select("//div[@id='footer']/child::p[position()=1]/text()").extract()
                tempDate = lastUpdateStringList[1].replace(":", " ").replace(",", " ")
                # convert to python time obj
                lastUpdateTime = datetime.strptime(tempDate, "%A %B %d %Y %I %M %p")
                # add item if old
                if today - lastUpdateTime > datetime.timedelta(days=30):
                    oldPage = CISEOldPages()

                    oldPage["url"] = response.url
                    oldPage["lastUpdated"] = lastUpdateStringList[1]
                    
                    return oldPage  

            # get links from the page and yield new requests

                pageLinks = sel.Select("//a/@href").extract()
                for link in pageLinks:
                    if "http://" not in link:
                        link = urlparse.urljoin(response.url, link.strip())
                for link in pageLinks:
                    if "mailto" not in link:
                        yield request(url=link, callback=self.parse_response)


        else:
            # log broken links
            deadLinks = CISEDeadLinks()
            title = sel.Select().extract()

            deadLinks['deadLinkURL'] = response.url
            #deadLinks['referrer'] = response.meta
            deadLinks['pageTitle'] = title

            return deadLinks


        #allow all domains (to test for broken links) but only get new links if wihtin jmu site 
        #sgml link extractor allow_domains (str or list) -  unique (boolean) – whether duplicate filtering should be applied to extracted links. 

        # response.status -> 200, 404 etc if 404, yeild item - if !200, yeild item with code and url