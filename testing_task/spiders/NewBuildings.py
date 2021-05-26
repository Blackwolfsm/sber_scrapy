import json

import scrapy
from scrapy.selector import Selector

from testing_task.items import BuildItem


class NewbuildingsSpider(scrapy.Spider):
    name = 'NewBuildings'
    allowed_domains = ['наш.дом.рф']
    start_urls = ['http://наш.дом.рф/сервисы/каталог-новостроек/список-объектов/список']

    def parse(self, response):
        item = BuildItem()
        data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').extract()[0]
        data = json.loads(data)
        houses = data['props']['initialState']['kn']['newbuildings']['houses']['data']['0']
        for house in houses:
            item['adress'] = house.get('objAddr')
            item['status'] = house.get('status')
            item['num_apartments'] = house.get('objElemLivingCnt')
            item['developer'] = house['developer']['fullName']  #изменить способ получения

            yield item
