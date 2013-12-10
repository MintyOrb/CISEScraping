BOT_NAME = 'CISEScraping'

SPIDER_MODULES = ['CISEScraping.spiders']
NEWSPIDER_MODULE = 'CISEScraping.spiders'
ITEM_PIPELINES = {
	'CISEScraping.pipelines.saveToFile':500,
	# 'CISEScraping.pipelines.twentyOldest':600,
	'CISEScraping.pipelines.emailResults':700
	}