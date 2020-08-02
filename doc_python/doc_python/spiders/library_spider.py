import scrapy
from ..items import DocumentationPythonItem


class LibrarySpiderSpider(scrapy.Spider):
    name = 'library'
    allowed_domains = ['docs.python.org/']
    start_urls = [
        'https://docs.python.org/zh-cn/3/library/index.html'
    ]

    def parse(self, response):
        urls = response.css('li.toctree-l2>a::attr(href)').extract()
        articles = []
        for url in urls:
            articles.append(url.split('#')[0])
        articles = set(articles)
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


