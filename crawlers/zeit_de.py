import re

from bs4 import BeautifulSoup

from itertools import dropwhile

from crawler import *

import re


class Article():        

    def get_teaser_data(self, article):

        self.link = article.get('href')

    def get_year_and_issue(self):

        a = re.findall('(20\d{2})[/-](\d{2})', self.link)

        year, issue = None, None

        if a:

            year, issue = a[0]

        return issue, year
    
    def get_article_data(self,request):

        if request.find('ol', class_="article-toc__list"):

            raise AttributeError

        try:

            self.date = re.match('.{10}', request.find('time').get('datetime')).group()

        except:

            self.date = None
        
        self.title = request.find('span',class_='article-heading__title')

        self.summary = request.find('div',class_='summary')

        x,y = self.get_year_and_issue()

        self.issue = 'DIE ZEIT, {0}/{1}'.format(x,y)
        
        self.author = request.find('span', itemprop='author')

        self.txt = ''.join([item.text for item in request.find_all('p', class_='paragraph article__item')])

        for instance in ('summary', 'title', 'author'):

            try:

                vars(self)[instance] = vars(self)[instance].get_text(strip = True)
                
            except AttributeError:

                vars(self)[instance] = ''
                
        if self.link.endswith('/komplettansicht'):

            self.link = self.link[:-16]
               

    def find_another_link(self, request):

        self.link += '/komplettansicht'



class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = [r.find('a') for r in bs_page.find_all('article', class_='teaser-small')]

        self.content_present = bool(self.teasers)

        if starting_page:

            if starting_page.endswith('/komplettansicht'):

                starting_page = starting_page[:-16]

            self.teasers = [ url for url in dropwhile(lambda x: x.get('href')!= starting_page, self.teasers) ]




class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.politicians = ('nicolas-sarkozy', 'françois-hollande', 'dmitri-medwedew', 'david-cameron', 'wladimir-putin', 'angela-merkel', 'theresa-may')
        
        self.storage = shelf['zeit_de']

        self.starting_page = 1

        self.data_format = '%Y-%m-%d'

        self.update_payload()

    def update_payload(self):

        self.site = 'http://www.zeit.de/thema/{0}?'.format(self.politicians[ self.storage['politNum'] ] )

        self.payload = {'p' : max(self.starting_page, self.storage['pn'])}
