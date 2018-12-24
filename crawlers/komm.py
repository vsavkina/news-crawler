from bs4 import BeautifulSoup

from crawler import Crawler

import datetime,re

from itertools import dropwhile


class Article():
    """
    Инициализирует парсер новостей сайта kommersant.ru
    """

    def __init__(self):

        pass

    def get_teaser_data(self, article):

        self.link = 'https://kommersant.ru' + article.find('h4', class_ = 'article_name').find('a').get('href')

        self.title = article.find('h4', class_ = 'article_name').text.strip()

        self.summary = article.find('div', class_ = 'text').text.replace('"', '')

        self.issue = article.find('p', class_ = 'b-main-search-results__src').find('a').text
    

    def get_article_data(self,request):

        try:

            self.date = request.find('time', class_ = 'b-article__publish_date').get('datetime')[:10]
        except:

            self.date = request.find('time', class_ = 'title__cake').get('datetime')[:10]
        self.author = '-'

        self.txt = ' '.join(x.text for x in request.find_all('p', class_="b-article__text"))            

    def find_another_link(self, request):

        return


class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find_all('article', class_='b-main-search-results__item ')

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: 'https://kommersant.ru' + x.find('h4', class_ = 'article_name').find('a').get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['komm']

        self.dateend = '26.03.2017' if self.storage['end_reached'][self.storage['politNum']] else self.storage['dateEnd']

        self.politicians = ('%ED%E8%EA%EE%EB%FF+%F1%E0%F0%EA%EE%E7%E8','%F4%F0%E0%ED%F1%F3%E0+%EE%EB%EB%E0%ED%E4','%E4%EC%E8%F2%F0%E8%E9+%EC%E5%E4%E2%E5%E4%E5%E2', '%E4%FD%E2%E8%E4+%EA%FD%EC%E5%F0%EE%ED', '%E2%EB%E0%E4%E8%EC%E8%F0+%EF%F3%F2%E8%ED', '%E0%ED%E3%E5%EB%E0+%EC%E5%F0%EA%E5%EB%FC', '%F2%E5%F0%E5%E7%E0+%EC%FD%E9')

        #self.politicians = ('николя саркози', 'франсуа олланд', 'дмитрий медведев', 'дэвид кэмерон', 'владимир путин', 'ангела меркель', 'тереза мэй')
        
        self.data_format = '%Y-%m-%d'

        self.starting_page = 1

        self.payload = {}

        self.update_payload()

    def update_payload(self):
        if self.storage['pn'] == 101:

            self.storage['pn'] = 1

            self.dateend = self.storage['dateEnd']
            
        self.site = r'https://www.kommersant.ru/Search/Results?search_query={}'.format(self.politicians[ self.storage['politNum'] ])
        self.payload = {'datestart' : '01.01.2000', 'dateend' : self.dateend, 'page' : max(self.starting_page, self.storage['pn'])}
