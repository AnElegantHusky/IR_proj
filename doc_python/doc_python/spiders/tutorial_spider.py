import scrapy
from ..items import DocumentationPythonItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TutorialSpiderSpider(CrawlSpider):
    name = 'tutorial'
    allowed_domains = ['python.org']
    start_urls = [
        'https://docs.python.org/zh-cn/3/tutorial/index.html',
    ]

    rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)]

    custom_settings = {
        'ITEM_PIPELINES': {
            'doc_python.pipelines.EnginePipeline': 300
        }
    }


    def parse_items(self, response):
        item = DocumentationPythonItem()
        item['title'] = ''.join(response.xpath('//title//text()').extract())
        item['body'] = ''.join(response.xpath('//body//text()').extract())
        item['url'] = response.url
        yield item

    # def parse(self, response):
    #     urls = response.css('div.body a::attr(href)').extract()
    #     articles = []
    #     for url in urls:
    #         articles.append(url.split('#')[0])
    #     articles = set(articles)
    #     for article in articles:
    #         url = response.urljoin(article)
    #         yield scrapy.Request(url=url, callback=self.doc_parse, dont_filter=True)




# class EngineSpiderSpider(scrapy.Spider):
#     name = 'engine'
#     allowed_domains = ['docs.python.org/']
#     start_urls = [
#         'https://docs.python.org/zh-cn/3/contents.html'
#     ]
#
#     custom_settings = {
#         'ITEM_PIPELINES': {
#             'doc_python.pipelines.EnginePipeline': 300
#         }
#     }
#
#     def parse(self, response):
#         urls = response.css('div#python-documentation-contents a::attr(href)').extract()
#         articles = []
#         for url in urls:
#             articles.append(url.split('#')[0])
#         articles = set(articles)
#         for article in articles:
#             url = response.urljoin(article)
#             yield scrapy.Request(url=url, callback=self.doc_parse, dont_filter=True)
#
#     def doc_parse(self, response):
#         item = DocumentationPythonItem()
#         item['title'] = ''.join(response.css('h1').css('::text').extract())
#         body = response.css('p, h2, h3')
#         body_text = ''
#         for p in body:
#             text = ''.join(p.css('::text').extract())
#             body_text += text + '\n'
#         item['body'] = body_text
#         item['url'] = response.url
#         yield item
#
