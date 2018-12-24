from bs4 import BeautifulSoup

from crawler import Crawler

import datetime

from itertools import dropwhile


class Article():
    """
    Инициализирует парсер новостей сайта ksta.de
    """

    def __init__(self):

        pass

    def get_teaser_data(self, article):

        daysOfWeek = {0:'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}

        self.date = article.find('time').get('datetime')[:10]

        year, month, day = map(int,self.date.split('-'))

        weekday = datetime.date(year, month, day).weekday()        

        self.link = 'http://www.ksta.de' + article.get('href')

        self.title = article.find('h3',class_='teaser_heading').text

        self.summary = article.find('p',class_='teaser_paragraph').text

        self.issue = "Kölner Stadt-Anzeiger, {}, {}".format(daysOfWeek[weekday], self.date[:10])
    

    def get_article_data(self,request):


        self.author = request.find('meta').get('content')

        self.txt = request.find('meta', property='articleBody').get('content')
            

    def find_another_link(self, request):

        self.link = 'http://www.ksta.de' + request.find('aside', class_='galleryReferrerList').find('a').get('href')


class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find('div', class_='dm_search_result_list').find_all('a',class_='normalTeaser')

        self.content_present = bool(self.teasers)

        if starting_page:

            self.teasers = [ url for url in dropwhile(lambda x: 'http://www.ksta.de' + x.get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['ksta_de']

        self.politicians = ('sarkozy','hollande','medwedew', 'cameron', 'putin', 'merkel', 'theresa+may')

        self.site = r'http://www.ksta.de/action/ksta/4484314/search?'

        self.data_format = '%Y-%m-%d'

        self.starting_page = 0

        self.update_payload()

    def update_payload(self):

        self.payload = {'pageNum' : max(self.starting_page, self.storage['pn']), 'query' : self.politicians[ self.storage['politNum'] ]}

    
