# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    url = scrapy.Field()
    date_time = scrapy.Field()
    news_info = scrapy.Field()
    body = scrapy.Field()
    id = scrapy.Field()
    # title = scrapy.Field()

    pass
