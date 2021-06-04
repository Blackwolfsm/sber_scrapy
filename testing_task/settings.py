import logging
from logging.handlers import RotatingFileHandler

from scrapy.utils.log import configure_logging


LOG_ENABLE = True
LOG_FILE = 'logs.log'

BOT_NAME = 'testing_task'

SPIDER_MODULES = ['testing_task.spiders']
NEWSPIDER_MODULE = 'testing_task.spiders'


ROBOTSTXT_OBEY = True

FEED_FORMAT = 'csv'
FEED_URI = 'buildings.csv'

ITEM_PIPELINES = {
    'testing_task.pipelines.EmptyFieldsPipeline': 100,
    'testing_task.pipelines.StatusBuildPipeline': 200,
    'testing_task.pipelines.ProcentSaleBuildPipeline': 300
}
