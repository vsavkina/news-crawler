"""
Инициализирует парсер новостей сайта spiegel.de
"""

from bs4 import BeautifulSoup

from crawler import Crawler

import re

import datetime

from itertools import dropwhile


class Article():

    def __init__(self):

        pass

    def get_teaser_data(self, article):       

        self.link = article.find('a').get('href')

        self.date = article.find('time').get_text(strip = True)[:10]

        if not re.match('\d{2}\.\d{2}\.\d{4}', self.date):

            self.date = None

        if not self.link.startswith('http'):

            self.link = 'http://www.sueddeutsche.de/' + self.link

        self.title = article.find('em',class_='entrylist__title')

        self.summary = article.find('p', class_ = 'entrylist__detail detailed-information')

        self.author = article.find('span', class_ = 'entrylist__author')

        for data in 'title', 'summary', 'author':

            try:

                vars(self)[data] = vars(self)[data].text.encode('utf-8', errors = 'ignore').decode('utf-8')

            except AttributeError:

                vars(self)[data] = None

        self.issue = 'Süddeutsche Zeitung, Di.' + str(self.date)
    

    def get_article_data(self,request):

        try:

            self.txt = request.find('div', id='article-body')

            self.txt = '\n'.join([t.text.encode('utf-8', errors = 'ignore').decode('utf-8') for t in self.txt.find_all('p', recursive = False)])

        except AttributeError:

            try:

                self.txt = request.find('section', class_='body')

                self.txt = '\n'.join([t.text.encode('utf-8', errors = 'ignore').decode('utf-8') for t in self.txt.find_all('p', recursive = False)])

            except AttributeError:

                self.txt = None


    def find_another_link(self, request):

        return
    

class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find_all('div', class_='entrylist__entry')

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: x.find('a').get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd = None):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['suedd']

        self.politicians = ('sarkozy', 'hollande', 'medwedew', 'cameron', 'putin', 'merkel', 'theresa+AND+may')

        self.starting_page = 1

        self.update_payload()

        self.data_format = '%d.%m.%Y'

        
    def update_payload(self):

        self.site = r'http://www.sueddeutsche.de/news/page/{}?'.format(max(self.starting_page, self.storage['pn']))

        self.payload = {'search' : self.politicians[ self.storage['politNum'] ], 'sort' : 'date', 'all[]' : 'dep', 'typ[]' : 'article', 'sys[]' : 'sz', 'catsz[]' : 'alles', 'all[]' : 'time' }

        
