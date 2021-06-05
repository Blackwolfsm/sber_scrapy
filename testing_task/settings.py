LOG_ENABLE = True
LOG_FILE = 'logs.log'

BOT_NAME = 'testing_task'

SPIDER_MODULES = ['testing_task.spiders']
NEWSPIDER_MODULE = 'testing_task.spiders'

RETRY_TIMES = 5
AUTOTHROTTLE_ENABLED = True

ROBOTSTXT_OBEY = True

FEED_FORMAT = 'csv'
FEED_URI = 'buildings.csv'

ITEM_PIPELINES = {
    'testing_task.pipelines.EmptyFieldsPipeline': 300,
    'testing_task.pipelines.StatusBuildPipeline': 100,
    'testing_task.pipelines.ProcentSaleBuildPipeline': 200
}
