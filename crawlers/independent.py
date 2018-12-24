from bs4 import BeautifulSoup

from crawler import Crawler

import datetime

from itertools import dropwhile


class Article():
    """
    Инициализирует парсер новостей сайта independent.co.uk
    """

    def __init__(self):

        pass

    def get_teaser_data(self, article):

        self.date = article.find('ul', class_="meta inline-pipes-list").find('li').get('title')[:10]      

        self.link = article.find('a').get('href')

        self.title = article.find('h2').text

        self.issue = "The Independent, {}".format(self.date)
    

    def get_article_data(self,request):


        self.author = request.find('li', class_='author').text

        self.summary = request.find('div',class_='intro').text.replace('"', '')

        self.txt = '\n'.join(t.text for t in request.find('div', class_='text-wrapper').find_all('p'))

        
    def find_another_link(self, request):

        return


class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find_all('li', class_='search-result')

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: x.find('a').get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['independent']

        self.politicians = ('nicolas sarkozy', 'francois hollande', 'dmitry medvedev', 'david cameron', 'vladimir putin', 'angela merkel', 'theresa may')

        self.site = r'http://www.independent.co.uk/search/site/{}'.format(self.politicians[ self.storage['politNum'] ])

        self.data_format = '%Y-%m-%d'

        self.starting_page = 0

        self.update_payload()

    def update_payload(self):

        self.site = r'http://www.independent.co.uk/search/site/{}'.format(self.politicians[ self.storage['politNum'] ])

        self.payload = {'page' : max(self.starting_page, self.storage['pn']) }

    
