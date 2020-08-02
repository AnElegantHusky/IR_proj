import scrapy
from ..items import DocumentationPythonItem


class DocumentationSpiderSpider(scrapy.Spider):
    name = 'documentation'
    allowed_domains = ['docs.python.org/']
    start_urls = [
        'https://docs.python.org/zh-cn/3/tutorial/index.html',
        'https://docs.python.org/zh-cn/3/reference/index.html',
        'https://docs.python.org/zh-cn/3/howto/index.html',
        'https://docs.python.org/zh-cn/3/faq/index.html',
    ]

    def parse(self, response):
        articles = response.css('li.toctree-l1>a::attr(href)').extract()
        for article in articles:
            url = response.url[:-10] + article
            yield scrapy.Request(url=url, callback=self.doc_parse, dont_filter=True)

    def doc_parse(self, response):
        item = DocumentationPythonItem()
        item['title'] = response.css('h1::text').extract_first()
        body = response.css('p')
        body_text = ''
        for p in body:
            text = ''.join(p.css('::text').extract())
            body_text += text + '\n'
        item['body'] = body_text
        item['url'] = response.url
        yield item


