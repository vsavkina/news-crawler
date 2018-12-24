from importlib import import_module

import shelve

from psycopg2 import DataError


def create_shelve():

    ModuleInfo = {'politNum': 0, 'pn' : 0, 'end_reached' : [0] * 7}

    return ModuleInfo



with shelve.open('shelf/temp.db', writeback = True) as s:
    
    modules = ('lemonde', 'guardian', 'independent', 'komm', 'vz', 'zeit_de', 'suedd', 'ksta_de', 'spiegel')

    pswd = 'admin'

    i = 0

    while i < len(modules):

        try:
            
            mod = import_module(modules[i])

            crawler = mod.News_crawler(s, pswd)

            crawler.crawl(modules[i])

            i += 1

        except KeyError as k:

            print(k)

            s[modules[i]] = create_shelve()

        except (KeyboardInterrupt, ConnectionError, AttributeError, DataError) as e:

            crawler.exit()

            print (e)

            break
    
