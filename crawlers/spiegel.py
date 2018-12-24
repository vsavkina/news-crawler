from bs4 import BeautifulSoup

from crawler import Crawler

import datetime

from itertools import dropwhile


class Article():

    """
    Инициализирует парсер новостей сайта spiegel.de
    """


    def __init__(self):

        pass

    def get_teaser_data(self, article):       

        self.link = article.find('a').get('href')

        if not self.link.startswith('http'):

            self.link = 'http://www.spiegel.de/' + self.link

        self.title = article.find('h2',class_='article-title')

        self.summary = article.find('p')

        self.issue = article.find('span',class_='source-date')
    

    def get_article_data(self,request):

        self.date = request.find('div', class_='spShortDate')           
        
        self.author = request.find('meta').get('content')

        for data in 'title', 'summary', 'issue', 'date', 'author':

            try:

                vars(self)[data] = vars(self)[data].text.encode('utf-8', errors = 'ignore').decode('utf-8')

            except AttributeError:

                vars(self)[data] = None

        if not self.date and self.issue:

            self.date = self.issue.strip()[-10:]

        try:

            self.txt = request.find('div', class_='article-section clearfix')

            self.txt = '\n'.join([t.text.encode('utf-8', errors = 'ignore').decode('utf-8') for t in self.txt.find_all('p', recursive = False)])

        except AttributeError:

            self.txt = request.find('div', class_='dig-text').text.encode('utf-8', errors = 'ignore').decode('utf-8')
            

    def find_another_link(self, request):

        return
    

class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find_all('div', class_='teaser')

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: 'http://www.spiegel.de/' + x.find('a').get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['spiegel']

        self.politicians = ('nicolas_sarkozy', 'francois_hollande', 'dmitrij_medwedew', 'david_cameron', 'wladimir_putin', 'angela_merkel', 'theresa_may')

        self.starting_page = 1

        self.data_format = '%d.%m.%Y'

        self.site = r'http://www.spiegel.de/thema/{}/dossierarchiv-{}.html'.format(self.politicians[ self.storage['politNum'] ], max(self.starting_page, self.storage['pn']))

        self.payload = None

    def update_payload(self):

        self.site = r'http://www.spiegel.de/thema/{}/dossierarchiv-{}.html'.format(self.politicians[ self.storage['politNum'] ], max(self.starting_page, self.storage['pn']))

    
