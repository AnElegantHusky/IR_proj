import scrapy
from ir_scrapy.items import NewsScrapyItem

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['tech.china.com/article']
    start_urls = ['https://tech.china.com/articles/']

    def parse(self, response):
        news_urls = response.css('div.wntjItem item_defaultView clearfix a::attr(href)')
        # urls = response.css('td.newblue1 a::attr(href)').extract()
        for url in news_urls:
            yield scrapy.Request(url=url, callback=self.doc_parse)
        next_page = response.css('div.pages a.a1::attr(href)').extract()[1]

    def doc_parse(self, response):
        pass
