import scrapy


class BuildItem(scrapy.Item):
    adress = scrapy.Field()
    status = scrapy.Field()
    num_apartments = scrapy.Field()
    developer = scrapy.Field()
    sale_apartments = scrapy.Field()
    avg_price = scrapy.Field()
    kadastr_nums = scrapy.Field()
