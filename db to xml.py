# coding: utf-8
from sql_functions import Db_manager
from lxml import etree
import os
import tokenizer, datetime

tables = ['lemonde', 'guardian', 'independent', 'komm', 'zeit_de', 'suedd', 'ksta_de', 'spiegel']
cols = ('id', 'link', 'title', 'summary', 'issue', 'author', 'date', 'politicians_mentioned', 'txt')
c = 0
ps = input('Input pswd: ')
for table in tables:
    path = r'C:\Users\user\Desktop\corpora\{}'.format(table)
    if not os.path.exists(path):
        os.makedirs(path)
    db = Db_manager(table, ps)
    db.connect()
    db.cur.execute('SELECT MAX(id) FROM {}'.format(table) )
    data = db.cur.fetchone()[0]
    c += int(data)
    """for row in data:
        row = list(row)
        row[-1], row[-2] = row[-2], row[-1]# swap text and politicians_mentioned
        if not row[-2]:
            print(row[0], row[1])
            continue
        name = row[0] #id
        with open(path + r'\{}.xml'.format(name), 'a', encoding = 'UTF-8') as f:
            if os.stat(path + r'\{}.xml'.format(name)).st_size == 0:
                root = etree.Element('article', attrib = {'id' : str(name), 'table' : table})
                polit_name=[n.split('|') for n in row[-2].split()]
                low = row[-1].lower()
                for name in polit_name[0]:
                    for sn in polit_name[1]:
                        if ' '.join( [name,sn] ) in low or ' '.join( [sn,name] ) in low:
                            c += 1
                            for i in range(1, len(cols)):
                                if isinstance(row[i], datetime.date):
                                    row[i] = row[i].strftime("%Y-%m-%d")
                                if not row[i]:
                                    row[i] = ' '
                                etree.SubElement(root, cols[i]).text = row[i].encode('utf-8', 'ignore').decode('utf-8')
                            """"""text = tokenizer.morph_tag(tokenizer.tokenize(row[-1], 'German') ,'de')
                            text_root = etree.SubElement(root, 'terminals')
                            for item in text:
                                etree.SubElement(text_root, 't', attrib = {'pos' : item.pos, 'lemma' : item.lemma} ).text = item.word

                            handle = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
                            f.writelines(handle)
                            break"""

    #db.disconnect()
print (c)
