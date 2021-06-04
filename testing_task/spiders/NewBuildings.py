import json
import logging
from json.decoder import JSONDecodeError
from typing import Collection

import scrapy
from scrapy.http import Request, request
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
from scrapy.http.response.html import HtmlResponse

from testing_task.items import BuildItem


OBJECTS_URL = ('https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%'
               'D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={collect}'
               '&limit=100')

CHECK_BUILD_URL = 'http://наш.дом.рф/сервисы/проверка_новостроек/'


class NewbuildingsSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy')
        logger.setLevel(logging.INFO)
        super().__init__(*args, **kwargs)
    
    name = 'NewBuildings'
    alowed_domains = ['xn--80az8a.xn--d1aqf.xn--p1ai']
    start_urls = [OBJECTS_URL.format(collect=0)]

    def parse(self, response, collect: int=None):
        collect = collect or 0
        data_json = self.response_to_json(response)
        total = data_json.get('data', {}).get('total')
        houses = data_json.get('data', {}).get('list')
        for house in houses:
            item = BuildItem()
            item['id_from_site'] = house.get('objId')
            item['adress'] = house.get('objAddr')
            item['status'] = house.get('objStatus')
            item['num_apartments'] = house.get('objElemLivingCnt')
            item['developer'] = house.get('developer', {}).get('fullName')
            collect += 1
            if item['status'] == 0:
                request = Request(
                    url=CHECK_BUILD_URL+str(item['id_from_site']),
                    callback=self.parse_check_house,
                    cb_kwargs=dict(item=item)
                )
                yield request

            else:
                yield item
        if collect < total:
            request = Request(url=OBJECTS_URL.format(collect=collect),
                              callback=self.parse,
                              cb_kwargs=dict(collect=collect))
            yield request
    
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
            logging.critical('На странице парсинга не найдены данные')
            raise CloseSpider('Возникла критическая ошибка')
        return data

    @staticmethod
    def response_to_json(response: HtmlResponse) -> dict:
        """Получает ответ запроса с объектами для парсинга,
           переводит данные в json.
        """
        try:
            data = response.json()
        except JSONDecodeError as e:
            logging.critical(f'При попытке декодировать json со страницы '
                             f'{response.url} возникла ошибка {e}')
            raise CloseSpider('Возникла критическая ошибка')
        return data
