from bs4 import BeautifulSoup

from crawler import Crawler

import datetime,re

from itertools import dropwhile


class Article():
    """
    Инициализирует парсер новостей сайта lenta.ru
    """

    def __init__(self):

        pass

    def get_teaser_data(self, article):  

        self.link = 'https://vz.ru' + article.find('a').get('href')

        try:
            
            y,m,d = re.findall('(\d{4})/(\d\d?)/(\d\d?)',self.link)[0]

        except:

            y,m,d = re.findall('(\d{4})\-(\d\d?)\-(\d\d?)',article.text)[0]

        self.date = '{}-{}-{}'.format(y,'0'+m if len(m) == 1 else m,'0'+d if len(d) == 1 else d)

        self.title = article.find('a').text.strip()

        self.summary = article.find('small').text.replace('"', '')

        self.issue = "vz.ru, {}".format(self.date)
    

    def get_article_data(self,request):


        self.author = '-'

        self.txt = request.find('div', class_="text").text
            

    def find_another_link(self, request):

        return


class Resultpage():

    def __init__(self):

        pass

    def gather_data(self, bs_page, starting_page):

        self.teasers = bs_page.find('ol')

        self.content_present = bool(self.teasers)

        if self.content_present:

            self.teasers = self.teasers.find_all('li')

            if starting_page:

                self.teasers = [ url for url in dropwhile(lambda x: 'https://vz.ru' + x.find('a').get('href')!= starting_page, self.teasers) ]


class News_crawler(Crawler):

    def __init__(self, shelf, pswd):

        Crawler.__init__(self, pswd)

        self.respage = Resultpage()

        self.article = Article()

        self.storage = shelf['vz']

        self.politicians = ('%ED%E8%EA%EE%EB%FF+%F1%E0%F0%EA%EE%E7%E8','%F4%F0%E0%ED%F1%F3%E0+%EE%EB%EB%E0%ED%E4','%E4%EC%E8%F2%F0%E8%E9+%EC%E5%E4%E2%E5%E4%E5%E2', '%E4%FD%E2%E8%E4+%EA%FD%EC%E5%F0%EE%ED', '%E2%EB%E0%E4%E8%EC%E8%F0+%EF%F3%F2%E8%ED', '%E0%ED%E3%E5%EB%E0+%EC%E5%F0%EA%E5%EB%FC', '%F2%E5%F0%E5%E7%E0+%EC%FD%E9')

        self.data_format = '%Y-%m-%d'

        self.starting_page = 1

        self.payload = {}

        self.update_payload()

    def update_payload(self):

        self.site = r'https://vz.ru/search/p{}/?action=search&s_string={}'.format(max(self.starting_page, self.storage['pn']), self.politicians[ self.storage['politNum'] ])
        self.payload = {}

    
