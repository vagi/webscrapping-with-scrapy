import scrapy
from protego import Protego


class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            card_details_uri = item.css('h2 > a::attr(href)').get()

            result = {
                'position': item.css('h2 > a::text').get(),
                'name': item.css('div > b::text').get(),
                # remove chars in age /'age': '18\xa0років'/ or process it before writing in csv file
                'age': item.css('div span:nth-child(4)::text').get(),
                'link': card_details_uri

            }

            # Remove salary once test is completed
            salary = item.css('h2 span.nowrap::text').get()
            if salary:
                result['salary'] = float(salary.replace(' грн', ''))

            yield response.follow(card_details_uri, self.parse_card_details, meta={
                'result': result
            })

    def parse_card_details(self, response):

        header = response.css('div.card > h2::text').get()

        description = ' '.join(response.css('div.card > p::text').getall())
        description = ' '.join(description.split())

        response.meta['result']['description'] = header + ': ' + description

        yield response.meta['result']
        
