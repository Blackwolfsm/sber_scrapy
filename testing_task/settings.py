import logging
from logging.handlers import RotatingFileHandler

from scrapy.utils.log import configure_logging


BOT_NAME = 'testing_task'

SPIDER_MODULES = ['testing_task.spiders']
NEWSPIDER_MODULE = 'testing_task.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'testing_task (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = True

FEED_FORMAT = 'csv'
FEED_URI = 'buildings.csv'

ITEM_PIPELINES = {
    'testing_task.pipelines.StatusBuildPipeline': 1,
    'testing_task.pipelines.ProcentSaleBuildPipeline': 2
}
