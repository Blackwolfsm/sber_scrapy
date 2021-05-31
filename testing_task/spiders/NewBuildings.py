import json
import logging
from json.decoder import JSONDecodeError

import scrapy
from scrapy.http import Request
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
from scrapy.http.response.html import HtmlResponse

from testing_task.items import BuildItem


class NewbuildingsSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='logs.log',
        filemode='w',
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    name = 'NewBuildings'
    allowed_domains = ['xn--80az8a.xn--d1aqf.xn--p1ai']
    start_urls = ['http://наш.дом.рф/сервисы/каталог-новостроек/список-объектов/список?page=0&limit=100']

    def parse(self, response):
        data = self.load_data(response)
        data = self.load_json(data)
        houses = (data
            .get('props', {})
            .get('initialState', {})
            .get('kn', {})
            .get('newbuildings', {})
            .get('houses', {})
            .get('data', {})
            .get('0')
        )
        for house in houses:
            item = BuildItem()
            item['adress'] = house.get('objAddr')
            item['status'] = house.get('status')
            item['num_apartments'] = house.get('objElemLivingCnt')
            item['developer'] = house.get('developer', {}).get('fullName')
            item['id_from_site'] = house.get('objId')

            if item['status'] == 0:
                request = Request(
                    url='http://наш.дом.рф/сервисы/проверка_новостроек/' + str(item['id_from_site']),
                    callback=self.parse_check_house,
                    cb_kwargs=dict(item=item)
                )
                yield request
            else:
                yield item
    
    def parse_check_house(self, response, item):
        data = self.load_data(response)
        data = self.load_json(data)
        card = (data
            .get('props', {})
            .get('initialState', {})
            .get('buildingsVerification', {})
            .get('houseCard')
        )
        item['sale_apartments'] = card.get('soldOutPerc')
        item['avg_price'] = card.get('objPriceAvg')
        parcels = []
        for parcel in card.get('parcel', {}):
            parcels.append(parcel.get('objParcel'))
        item['kadastr_nums'] = parcels

        yield item

    @staticmethod
    def load_json(data: str) -> dict:
        """Принимает строку данных, переводит в json"""
        try:
            data = json.loads(data)
        except JSONDecodeError as e:
            logging.critical(f'При декодировании данных со страницы'
                             f'в json возникла ошибка {e}')
            raise CloseSpider('Возникла критическая ошибка')

        return data
    
    @staticmethod
    def load_data(response: HtmlResponse) -> str:
        """Находит данные в ответе, возвращает готовую строку"""
        try:
            data = (response
                .xpath('//*[@id="__NEXT_DATA__"]/text()')
                .extract()[0]
            )
        except IndexError:
            logging.critical('На странице парсинга не найдены json данные')
            raise CloseSpider('Возникла критическая ошибка')
        return data
