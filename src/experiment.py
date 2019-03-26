# coding=utf-8

import json
from collections import Counter
from filepathConfig import *
from nltk.tokenize import RegexpTokenizer
from gensim import corpora
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from projectSelect.smallcorpusTrain import smallCorpusTrain
import re

# basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/10个项目的对比方法实验/'
# projectDict = {'angular': 45, 'bitcoin': 67, 'elasticsearch': 40, 'owncloud': 39, 'pydata': 40, 'rails': 64,
#                'RIOT-OS': 39, 'symfony': 70, 'tgstation': 30, 'ceph': 32}
# for projectName in projectDict:
#     if projectName != 'ceph':
#         continue
#     projectFile = projectName + '项目实验/'
#     # for i in xrange(1, projectDict[projectName] + 1):
#     for i in xrange(1, 2):
#         trainNumberFile = '第' + str(i) + '次训练/'
#         trainBasicFile = basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
#         testBasicFile = basicFilepath + projectFile + trainNumberFile + 'testCorpus/'
#         trainWord = unicode(trainBasicFile + 'tag.txt', 'utf-8')
#         # testWord = unicode(testBasicFile + 'testCorpus_word.txt', 'utf-8')
#         i = 0
#         with open(trainWord,'r') as e:
#             for line in e:
#                 data = json.loads(line)
#                 if data.__len__() != 0:
#                     i+=1
#         print i


import re
import codecs

class Corpus:
    def __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        with codecs.open(self.dirname,'r','utf-8') as e:
            for line in e:
                data = json.loads(line)
                # resLs = [val for val in data if not re.match('\d*',val)]
                yield data

def getDoc_set_First(trainCorpusSentence):
    deleteWord = ['<', '>', '>=', '<=', '-', '+', '*']

    reg1 = re.compile('[\r\n\"]')
    reg3 = re.compile(' +')
    reg4 = re.compile('^ ')
    # reg5 = re.compile('(`\w+`)')
    code1_reg = re.compile('(`[\w\-\.\*/:]+`)')
    code2_reg = re.compile('(```[\s\S]+?```)')
    code3_reg = re.compile('(\.\.\.[\s\S]+?\.\.\.)')
    code4_reg = re.compile('(\*\*[\s\S]+?\*\*)')

    img_reg = re.compile('(<img[\s\S]+?>)')
    link_reg = re.compile(r'(https?://[\w\.\-/]+)')

    function_reg = re.compile('([\w\_]+\(.*?\))')  ###取出函数

    res = re.compile("[\[*\]*\)\(>;_\|*]")  ##消除word中的字符
    res2 = re.compile('^\d[\d.]+\d$')
    res3 = re.compile('\*|`|-|##+|\[|\]|&+|\?|~|/|!=|\.|\\\\+|<+|=+')
    replaceStr = [u"“", u'– ', u"”", u"→", u"–", "(", u" ", u'🎵', u'©', u'😞', u'…', u"‘", u"’", u"²"]

    ###去除首部空格
    lineNumber = 0
    for doc in trainCorpusSentence:
        lineNumber += 1
        doc[0] = re.sub(img_reg, '', doc[0])  ## 去掉图片

        doc[0] = re.sub(reg1, ' ', doc[0])  ## 去掉\r \n
        doc[0] = doc[0].strip('.')
        wordLs = []

        for word in code1_reg.findall(doc[0]):
            wordLs.append(word)
            doc[0] = doc[0].replace(word, '')
        for word in code2_reg.findall(doc[0]):  ###一块区域的函数
            for subword in function_reg.findall(word):
                wordLs.append(subword)
                word = word.replace(subword, '')
            wordLs.extend(word.strip().split(' '))
            doc[0] = doc[0].replace(word, '')
        for word in code3_reg.findall(doc[0]):
            for subword in function_reg.findall(word):
                wordLs.append(subword)
                word = word.replace(subword, '')
            wordLs.extend(word.strip().split(' '))
            doc[0] = doc[0].replace(word, '')
        for word in link_reg.findall(doc[0]):  ##  取出链接
            wordLs.append(word)
            doc[0] = doc[0].replace(word, '')

        doc[0] = re.sub(reg3, ' ', doc[0])  ##去除空格
        doc[0] = re.sub(reg4, '', doc[0])  ##去除首部空格

        doc[0] = doc[0].replace(u"’s", " is")
        doc[0] = doc[0].replace("\u2019s", " is")
        doc[0] = doc[0].replace(u"’re", " are")
        doc[0] = doc[0].replace("\u2019re", " are")
        doc[0] = doc[0].replace(u"’m", " am")
        doc[0] = doc[0].replace("\u2019m", " am")
        doc[0] = doc[0].replace(u"n’t", " not")
        doc[0] = doc[0].replace("n\u2019t", " not")
        for val in replaceStr:
            doc[0] = doc[0].replace(val, "")
        # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

        tmpWordLs = doc[0].lower().strip().split(' ')
        en_stop = get_stop_words("en")
        stopped_tokens = [word.strip(",:.") for word in tmpWordLs if word not in en_stop]
        p_stemmer = PorterStemmer()
        texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
        texts.extend(wordLs)

        res_text = []
        for word in texts:
            word = word.replace(" ", "")
            if isinstance(word,unicode):
                for tmpStr in replaceStr:
                    word = word.replace(tmpStr,"")
            else:
                word = word.replace('\u2018', "")
                word = word.replace('\u2019', "")
            word = re.sub(res, '', word)
            word = re.sub(res2, '', word)
            word = re.sub(res3, '', word)
            if word.__len__() > 1 and word not in en_stop:
                res_text.append(word)
        print(res_text)

if __name__ == '__main__':
    sentences = Corpus('../src/text')
    getDoc_set_First(sentences)
    print(u'\u0142')