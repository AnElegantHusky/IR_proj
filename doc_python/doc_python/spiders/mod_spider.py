import scrapy
import re
from ..items import DocumentationPythonItem
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urlparse


class ModSpiderSpider(scrapy.Spider):
    name = 'mod'
    allowed_domains = ['docs.python.org/']
    start_urls = [
        'https://docs.python.org/zh-cn/3/contents.html'
    ]

    def parse(self, response):
        urls = response.css('div#python-documentation-contents a::attr(href)').extract()
        articles = []
        for url in urls:
            articles.append(url.split('#')[0])
        articles = set(articles)
        for article in articles:
            url = response.urljoin(article)
            yield scrapy.Request(url=url, callback=self.doc_parse, dont_filter=True)

    def doc_parse(self, response):
        item = DocumentationPythonItem()
        item['title'] = ''.join(response.css('h1').css('::text').extract())
        body = response.css('p, h2, h3')
        body_text = ''
        for p in body:
            text = ''.join(p.css('::text').extract())
            body_text += text + '\n'
        item['body'] = body_text
        item['url'] = response.url
        yield item


