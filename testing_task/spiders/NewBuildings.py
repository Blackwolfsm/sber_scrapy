import json

import scrapy
from scrapy.http import Request

from testing_task.items import BuildItem


class NewbuildingsSpider(scrapy.Spider):
    name = 'NewBuildings'
    allowed_domains = ['xn--80az8a.xn--d1aqf.xn--p1ai']
    start_urls = ['http://наш.дом.рф/сервисы/каталог-новостроек/список-объектов/список?page=0&limit=100']

    def parse(self, response):
        data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').extract()[0]
        data = json.loads(data)
        houses = data['props']['initialState']['kn']['newbuildings']['houses']['data']['0'] #повесить try
        for house in houses:
            item = BuildItem()
            item['adress'] = house.get('objAddr')
            item['status'] = house.get('status')
            item['num_apartments'] = house.get('objElemLivingCnt')
            item['developer'] = house.get('developer', {}).get('fullName')
            house_id = house.get('objId')

            if item['status'] == 0:
                request = Request(
                    url='http://наш.дом.рф/сервисы/проверка_новостроек/' + str(house_id),
                    callback=self.parse_check_house,
                    cb_kwargs=dict(item=item)
                )
                yield request
            else:
                yield item
    
    def parse_check_house(self, response, item):
        data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').extract()[0]
        data = json.loads(data)
        card = data.get('props', {}).get('initialState', {}).get('buildingsVerification', {}).get('houseCard') #повесить try
        item['sale_apartments'] = card.get('soldOutPerc')
        item['avg_price'] = card.get('objPriceAvg')
        parcels = []
        for parcel in card.get('parcel', {}):
            parcels.append(parcel.get('objParcel'))
        item['kadastr_nums'] = parcels

        yield item
