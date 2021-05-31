import scrapy


class BuildItem(scrapy.Item):
    id_from_site = scrapy.Field()
    adress = scrapy.Field()
    status = scrapy.Field()
    num_apartments = scrapy.Field()
    developer = scrapy.Field()
    sale_apartments = scrapy.Field()
    avg_price = scrapy.Field()
    kadastr_nums = scrapy.Field()
