"""
Суперкласс для всех кроулеров. 
"""

from bs4 import BeautifulSoup

import requests, collections, datetime

import sql_functions as sql

class Crawler():


    def __init__(self, pswd):

        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

        self.pswd = pswd


    def crawl(self, tablename):

        self.open_database(tablename)

        self.db.create_table()

        for polit_index in range(self.storage['politNum'],len(self.politicians)):

            self.update_payload()

            self.curr_pol = polit_index

            self.get_links(polit_index, self.storage['end_reached'][polit_index])

            self.storage['end_reached'][polit_index] = False

            print('Starting ', self.politicians[polit_index])

            self.crawl_over_pages()

            self.storage['politNum'] += 1

            self.storage['end_reached'][polit_index] = True

            self.storage['pn'] = self.starting_page

            if 'dateEnd' in self.storage:

                self.dateend = '26.03.2017'

        self.storage['politNum'] = 0

        self.exit()


    def open_database(self, tablename):

        self.db = sql.Db_manager(tablename, self.pswd)

        self.db.connect()


    def get_links(self, index, end_reached):

        self.db.get_first_and_last_links(index, end_reached)

        self.earliest = self.db.earliest

        self.latest = self.db.latest

        self.last_query_date = self.db.latest_date
        

    def do_search(self):
        
        searchpage = self.request_and_soupify(params = self.payload)

        self.process_pages(searchpage)


    def request_and_soupify(self, link = None, params = None):

        rqst = requests.get(self.site if not link else link, params, headers = self.headers)

        res = BeautifulSoup(rqst.text, "html.parser")
        
        return res


    def go_to_new_page(self):

        self.do_search()

        self.storage['pn'] += 1

        self.update_payload()


    def crawl_over_pages(self):

        self.all_pages_crawled = False

        while not self.all_pages_crawled:

            print ('Page:', self.storage['pn'])

            self.go_to_new_page()

        print ('All crawled')


    def process_pages(self, page):

        pg = self.respage

        pg.gather_data(page, self.earliest)

        if 'last_page' in vars(pg) and int(pg.last_page) + 1 < self.storage['pn']:

            self.all_pages_crawled = True

            return

        results = pg.teasers

        if not results:

            if not pg.content_present:

                self.all_pages_crawled = True

            return

        if self.earliest:

            results.pop(0)

            print('---')

            self.earliest = None

        for teaser in results:

            data = self.article

            data.get_teaser_data(teaser)

            rq = self.request_and_soupify(data.link)

            if not rq:

                continue

            try:

                data.get_article_data(rq)

            except AttributeError:

                try:

                    data.find_another_link(rq)

                    rq = self.request_and_soupify(data.link)

                    data.get_article_data(rq)

                except:

                    with open('links.txt', 'a') as f:

                        f.write(data.link)

            if data.link == self.latest or (data.date and datetime.datetime.strptime(data.date, self.data_format).date() < self.last_query_date):

                self.all_pages_crawled = True

                return

            if 'dateEnd' in self.storage:

                self.storage['dateEnd'] = '.'.join(data.date.split('-')[::-1])

            self.db.write_data(vars(data), self.curr_pol)

            print(data.link)


    def exit(self):

        self.db.handle_duplicates()

        self.db.disconnect()

        

        

            
