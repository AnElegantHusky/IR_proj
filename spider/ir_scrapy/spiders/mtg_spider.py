import scrapy


class MtgSpiderSpider(scrapy.Spider):
    name = 'mtg_spider'
    allowed_domains = ['magic.wizards.com/en']
    start_urls = ['https://magic.wizards.com/en/']

    def parse(self, response):
        pass
