import scrapy
from protego import Protego



class CvWorkUaSpider(scrapy.Spider):
    name = 'cv_work_ua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    def parse(self, response):
        '''
        This method parses required information, i.e. full_name, position, age, link to personal
        card, clean it and collect into dictionary, then calls method parse_card_details to collect
        description of each job seeker's work experience, and then crawls from page to page using
        pagination and recurcevely collect the said information
        :param
        response: Scrapy object
        :return:
        result : dictionary
            contains all collected and cleaned information
        '''

        # Iterate through cards of job seekers
        for item in response.css('div#pjax-resume-list div.card.resume-link'):

            # Getting url link of each job seeker's card
            card_details_uri = item.css('h2 > a::attr(href)').get()

            # Getting and cleaning data regarding an age of a candidate
            age_raw = item.css('div span:nth-child(4)::text').get()[:2]
            if age_raw.strip().isdigit():
                age = int(age_raw)
            else:
                age_raw = item.css('div span:nth-child(3)::text').get()[:2]
                age = int(age_raw)

            # Collecting and cleaning information regarding salary
            salary = item.css('h2 span.nowrap::text').get()
            salary = float(salary.replace(' грн', '')) if salary else None

            # Building a dictionary with collected information
            result = {
                'full_name': item.css('div > b::text').get(),
                'position': item.css('h2 > a::text').get(),
                'age': age,
                'salary': salary,
                'link': card_details_uri,
            }

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
        '''
        This method parse detailed information about job seeker's work experience
        from her/his personal card and add the description to the dictionary 'result'
        :param response:
        :return:
        result : dictionary
        '''

        header = response.css('div.card > h2::text').get()
        description = ' '.join(response.css('div.card > p::text').getall())
        description = ' '.join(description.split())
        response.meta['result']['description'] = header + ': ' + description

        yield response.meta['result']
