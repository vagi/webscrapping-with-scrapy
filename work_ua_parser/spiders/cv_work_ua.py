import scrapy
from protego import Protego


class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        for item in response.css('div#pjax-resume-list div.card.resume-link'):
            print(item.css('h2 a::text').get())
        
