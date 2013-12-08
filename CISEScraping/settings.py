BOT_NAME = 'CISEScraping'

SPIDER_MODULES = ['CISEScraping.spiders']
NEWSPIDER_MODULE = 'CISEScraping.spiders'
ITEM_PIPELINES = {'CISEScraping.pipelines.saveToFile':500}