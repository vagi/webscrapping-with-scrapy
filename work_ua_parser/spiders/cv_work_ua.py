import scrapy
from protego import Protego


class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            result = {
                'position': item.css('h2 > a::text').get(),
                'name': item.css('div > b::text').get(),
                'age': item.css('div > span:nth-child(4)::text').get(),

            }

            salary = item.css('h2 span.nowrap::text').get()

            if salary:
                result['salary'] = float(salary.replace(' грн', ''))

            yield result
        
