from nltk.tokenize import sent_tokenize, word_tokenize
import treetaggerwrapper
import xml.etree.ElementTree as ET
from random import shuffle

def tokenize(text, lng):

    sent_tok = [x.strip() for x in sent_tokenize(text, lng)]

    sent_and_wordforms = ['\n'.join(word_tokenize(t, lng)) for t in sent_tok]

    return sent_and_wordforms

#morphological tagging

def morph_tag(sentences, lng):

    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lng)

    tags = tagger.tag_text(sentences, tagonly = True)

    tags2 = treetaggerwrapper.make_tags(tags)

    return tags2


#syntactical tagging
def synt_tag(root):

    res = {}

    punct = []
    
    #Создадим итераторы, проходящие по терминальным и нетерминальным вершинам графа

    term, non_term = root.iter('terminals'), root.iter('nonterminals')

    #Проходим по всем графам синтаксической структуры

    for nonterminal in non_term:

        #Вызываем элемент terminals, ооответствующий тому же тексту, что и граф синт.структуры (одновременно вызываем дерево и список токенов)

        next_term = next(term)

        #Проходим по всем нетерминальным элементам дерева

        for nt in nonterminal.findall('*'):

            if nt.attrib['cat'] not in res:

                res[nt.attrib['cat']] = []

            temp = ''

            for edge in nt.iter('edge'):

                i = edge.attrib['idref']

                tag = '{} '.format(next_term.find(".t[@id=\"{}\"]".format(i)).attrib['pos'] if int(i.split('_')[1]) < 500 else nonterminal.find(".nt[@id=\"{}\"]".format(i)).attrib['cat'])

                if tag.startswith('$'):

                    if not tag in punct:

                        punct.append(tag)

                    tag = str(punct.index(tag)) + ' '

                temp += tag
                
            if temp not in res[nt.attrib['cat']]:

                res[nt.attrib['cat']].append(temp)

    r = ''
    for nt in 'VROOT', 'S':
        
        r += '{} -> {}\n'.format(nt, ' | '.join(res.pop(nt)))

    r += '\n'.join([' -> '.join((k, ' | '.join(v))) for k,v in res.items()])

    return r

"""parser = ET.XMLParser(encoding = 'UTF-8')           
tree = ET.parse('tiger_release_aug07.xml', parser = parser)
root = [ t for t in tree.getroot() ]
shuffle(root)
root = (i for i in root[:5000])
with open('grammar.txt', 'w') as f:
    f.write(synt_tag(root))"""
