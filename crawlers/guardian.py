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

            self.link = 'https://www.theguardian.com/' + self.link

        self.title = article.text

    

    def get_article_data(self,request):

        self.summary = request.find('div', class_ = 'gs-container').text

        self.date = request.find('time', itemprop='datePublished').get('datetime')[:10]

        try:
        
            self.author = request.find('span', itemprop='author').text

        except:

            self.author = ' '

        self.issue = 'The Guardian, {}'.format(self.date)

        try:

            self.txt = request.find('div', class_='content__article-body').find_all('p')

        except:

            self.txt = ' '

        self.txt = '\n'.join(t.text for t in self.txt)

            

    def find_another_link(self, request):

        return
    

class Resultpage():

    def __init__(self):


        pass

    def gather_data(self, bs_page, starting_page):

    
        self.last_page = bs_page.find('div', class_='pagination__list').find_all(class_="button")[:5][-1].text

        self.teasers = bs_page.find_all('h2', class_="fc-item__title")

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: x.find('a').get('href')!= starting_page, self.teasers) ]



class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['guardian']

        self.politicians = ('nicolas-sarkozy', 'francois-hollande', 'dmitry-medvedev', 'davidcameron', 'vladimir-putin', 'angela-merkel', 'theresamay')

        self.local = (3, 6)

        self.starting_page = 1

        self.data_format = '%Y-%m-%d'

        self.site = r'https://www.theguardian.com/{}/{}?'.format('world' if self.storage['politNum'] not in self.local else 'politics', self.politicians[ self.storage['politNum'] ])


    def update_payload(self):

        self.payload = {'page' : max(self.starting_page, self.storage['pn']) }

        self.site = r'https://www.theguardian.com/{}/{}?'.format('world' if self.storage['politNum'] not in self.local else 'politics', self.politicians[ self.storage['politNum'] ])

    
