from scrapy import signals
from tqdm import tqdm

from itemadapter import is_item, ItemAdapter


class StatusBarSpiderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        self.pbar = tqdm()
        self.pbar.clear()
        self.pbar.write(f'Паук {spider.name} начал работу')

    def spider_closed(self, spider):
        self.pbar.clear()
        self.pbar.write(f'Паук {spider.name} закончил работу')
        self.pbar.close()
