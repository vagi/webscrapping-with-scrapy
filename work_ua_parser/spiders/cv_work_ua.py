import scrapy
from protego import Protego


class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            # Getting url link for each candidacy's card
            card_details_uri = item.css('h2 > a::attr(href)').get()

            # Building a dictionary with collected inforamtion
            result = {
                'position': item.css('h2 > a::text').get(),
                'full_name': item.css('div > b::text').get(),
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
        # Pagination - crawling to next page of the resource
        for page in response.css('ul.pagination li'):
            # Looking for tag with text "Next Page"
            if page.css('a::text').get() == 'Наступна':
                # Getting url of the next page
                yield response.follow(
                    page.css('a::attr(href)').get(),
                    self.parse
                )

    def parse_card_details(self, response):

        header = response.css('div.card > h2::text').get()

        description = ' '.join(response.css('div.card > p::text').getall())
        description = ' '.join(description.split())

        response.meta['result']['description'] = header + ': ' + description

        yield response.meta['result']
        
