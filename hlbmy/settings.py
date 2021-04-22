BOT_NAME = 'hlbmy'
SPIDER_MODULES = ['hlbmy.spiders']
NEWSPIDER_MODULE = 'hlbmy.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
ITEM_PIPELINES = {
    'hlbmy.pipelines.DatabasePipeline': 300,
}
FEED_EXPORT_ENCODING = 'utf-8'

LOG_LEVEL = 'WARNING'

# LOG_LEVEL = 'DEBUG'
