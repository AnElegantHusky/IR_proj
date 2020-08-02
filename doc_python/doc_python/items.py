# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
sys.path.append("../")
from engine.elasticsearch_orm import engineMiddleware

class DocumentationPythonItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()

    def save_to_es(self):
        middleware = engineMiddleware()
        middleware.title = self['title']
        middleware.body = self['body']
        middleware.url = self['url']
        middleware.save()
        return