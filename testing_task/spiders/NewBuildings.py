import scrapy


class NewbuildingsSpider(scrapy.Spider):
    name = 'NewBuildings'
    allowed_domains = ['наш.дом.рф']
    start_urls = ['http://наш.дом.рф/']

    def parse(self, response):
        pass
