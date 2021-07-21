import scrapy


class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['http://work.ua/']

    def parse(self, response):
        pass
