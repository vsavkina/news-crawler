import psycopg2, datetime

pols = ('sarkozy nicolas', 'hollande françois|francois', 'medwedew|medvedev dmitry|dmitrij|dmitri', 'cameron david', 'putin vladimir|wladimir', 'merkel angela', 'may theresa')

class Db_manager():

    def __init__(self, tablename, pswd = None):

        self.database = 'corpora'

        self.user = 'postgres'

        self.pswd = input('Input password for postgres:')if not pswd else pswd

        self.tablename = tablename

    def connect(self):

        self.conn = psycopg2.connect("dbname={} user={} password={}".format(self.database, self.user, self.pswd))

        self.cur = self.conn.cursor()

    def create_table(self):

        self.cur.execute("CREATE TABLE IF NOT EXISTS {} (id serial PRIMARY KEY not null, link text, title text, summary text, issue text, author text, date date, txt text, politicians_mentioned text);".format(self.tablename))

    def get_first_and_last_links(self, pol_index, end_reached):

        #значения по умолчанию

        self.earliest, self.latest, self.latest_date = None, None, datetime.date(1100, 1, 1)

        date = datetime.date(2100, 1, 1)
            
            #возвращает ссылку на последнюю занесенную в ДБ статью об искомом политике

        try:

            if not end_reached:

                self.cur.execute("SELECT link, date FROM {} WHERE politicians_mentioned = '{}' ORDER BY id DESC".format(self.tablename, pols[pol_index]))

                self.earliest, date = self.cur.fetchone()


            #возвращает самую свежую запись об искомом политике

            self.cur.execute("SELECT link, date FROM {} WHERE politicians_mentioned = '{}' and date < '{}' ORDER BY date DESC, id DESC".format(self.tablename, pols[pol_index], date))

            self.latest, self.latest_date = self.cur.fetchone()


        except TypeError as e: #возникает только тогда, когда БД пуста

            pass

        print ('starting point = {}, end_point = {}'.format(self.earliest, self.latest))
            

    def write_data(self, d, pol_index):

        d['politicians_mentioned'] = pols[pol_index]

        query = "INSERT INTO {} ({}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(self.tablename, ', '.join(d.keys()))
                
        data = tuple(d.values())

        #print(d.keys())

        try:
                
            self.cur.execute(query, data)

        except UnicodeEncodeError:

            d['txt'] = ' '

            data = tuple(d.values())

            self.cur.execute(query, data)


        self.conn.commit()
                         
    def disconnect(self):

        self.cur.close()

        self.conn.close()

    def handle_duplicates(self):

        # для каждой статьм, встречающейся более, чем 1 раз, добавляет в первую содержащую ее строку

        # полный список упомянутых в ней политиков

        print ('Handling...')

        """query1 = UPDATE {0}

SET

politicians_mentioned = x.politicians_mentioned

FROM

(SELECT MIN(id) AS id, politicians_mentioned FROM (SELECT id, link, string_agg(politicians_mentioned, ', ') AS politicians_mentioned FROM {0} GROUP BY id) AS foo GROUP BY link, politicians_mentioned) x

WHERE

{0}.id = x.id

"""
        # удаляет все дубликаты

        query = "DELETE FROM {0} WHERE id NOT IN (SELECT MIN(id) as id FROM {0} GROUP BY link);"

        #for query in query1, query2:

        print (query[0:6])

        self.cur.execute(query.format(self.tablename))

        self.conn.commit()




