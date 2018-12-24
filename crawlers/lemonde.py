from bs4 import BeautifulSoup

from crawler import Crawler

import datetime,re

from itertools import dropwhile


class Article():

    """
    Инициализирует парсер новостей сайта theguardian.com    """


    def __init__(self):

        pass

    def get_teaser_data(self, article):       

        self.link = article.find('a').get('href')

        if not self.link.startswith('http'):

            self.link = 'http://www.lemonde.fr' + self.link

        self.title = article.find('h3').text

        self.issue = article.find('span', class_ = 'txt1 signature').text

        self.summary = article.find('p').text

    

    def get_article_data(self,request):

        self.date = request.find('time', itemprop='datePublished').get('datetime')[:10] 

        request = request.find('div', id='articleBody')

        try:
            request.h2.name = 'p'
        except:
            pass
        try:
            self.txt = request.find_all('p')

            self.txt = '\n'.join(t.text for t in self.txt)
        except:

            self.txt = ''

        try:
        
            self.author = request.find('span', class_='identite').find('a', class_='gras').text
        except:
           self.author = ' '



            

    def find_another_link(self, request):

        return
    

class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find_all('article', class_="grid_12 alpha enrichi mgt8")

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: 'http://www.lemonde.fr' + x.find('a').get('href')!= starting_page, self.teasers) ]



class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['lemonde']

        self.politicians = ('nicolas sarkozy', 'francois hollande', 'dmitry medvedev', 'david cameron', 'vladimir putin', 'angela merkel', 'theresa may')

        self.starting_page = 1

        self.data_format = '%Y-%m-%d'

        self.site = r'http://www.lemonde.fr/recherche/?operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=custom_date&start_day=01&start_month=01&start_year=2000&end_day=28&end_month=03&end_year=2017&sort=desc'.format(self.politicians[ self.storage['politNum'] ])


    def update_payload(self):

        self.payload = {'keywords' : self.politicians[ self.storage['politNum'] ], 'page_num' : max(self.starting_page, self.storage['pn']) }


    
