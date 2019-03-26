#coding=utf-8

import codecs
import json

from gensim import corpora
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from projectSelect.smallcorpusTrain import smallCorpusTrain
import re

class Corpus:
    def __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        with codecs.open(self.dirname,'r','utf-8') as e:
            for line in e:
                data = json.loads(line)
                # resLs = [val for val in data if not re.match('\d*',val)]
                yield data

class Tags:
    def __init__(self,dirname):
        self.dirname = dirname

    def __iter__(self):
        with codecs.open(self.dirname,'r','utf-8') as e:
            lineNumber = -1
            for line in e:
                lineNumber+=1
                data = json.loads(line)
                # resLs = [val for val in data if not re.match('\d*',val)]
                yield {lineNumber:data}

    @classmethod
    def getDict(cls,dirname):
        retDict = {}
        try:
            with codecs.open(dirname,'r','utf-8') as e:
                lineNumber = -1
                for line in e:
                    lineNumber+=1
                    data = json.loads(line)
                    retDict[lineNumber] = [ls[0] for ls in data]
                    # resLs = [val for val in data if not re.match('\d*',val)]
        except Exception,e1:
            print dirname
        return retDict

    @classmethod
    def getDict1(cls,dirname):
        retDict = {}
        with codecs.open(dirname,'r','utf-8') as e:
            lineNumber = -1
            for line in e:
                lineNumber+=1
                data = json.loads(line)
                retDict[lineNumber] = data
                # resLs = [val for val in data if not re.match('\d*',val)]
        return retDict

class TokenWord:

    """得到每个doc中的word"""
    @staticmethod
    def getDoc_set(trainCorpusSentence,testCorpusSentence,trainWord,testWord):

        tokenizer = RegexpTokenizer(r'\w+')
        res = re.compile(r'(http://[\w\.\-/]+)')
        res1 = re.compile(r'((\w+\-)+\w+)')
        res2 = re.compile(r'(\w+\.\w+)|(\d+ns)')
        res3 = re.compile(r'#\d+')

        with open(trainWord,'w') as e:
            lineNumber = 0
            for doc in trainCorpusSentence:
                lineNumber += 1

                doc[0] = doc[0].replace("'s"," is")
                doc[0] = doc[0].replace("'re"," are")
                doc[0] = doc[0].replace("'m"," am")
                doc[0] = doc[0].replace("n't"," not")
                tmpWordLs = []

                for word in res.findall(doc[0]):
                    tmpWordLs.append(word)
                    doc[0] = doc[0].replace(word, '')
                for wordLs in res1.findall(doc[0]):
                    tmpWordLs.append(wordLs[0])
                    doc[0] = doc[0].replace(wordLs[0], '')
                for wordLs in res2.findall(doc[0]):
                    for word in wordLs:
                        if word != '':
                            tmpWordLs.append(word)
                            doc[0] = doc[0].replace(word, '')
                for word in res3.findall(doc[0]):
                    tmpWordLs.append(word)
                    doc[0] = doc[0].replace(word, '')

                raw = doc[0].lower()
                tokens = tokenizer.tokenize(raw)
                en_stop = get_stop_words("en")
                stopped_tokens = [i for i in tokens if i not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
                texts.extend(tmpWordLs)

                for word in texts:
                    if word.__len__() == 1:
                        print('train',word)
                        print(lineNumber)
                        break

                e.write(json.dumps(texts)+'\n')
        with open(testWord,'w') as e:
            for doc in testCorpusSentence:
                doc[0] = doc[0].replace("'s", " is")
                doc[0] = doc[0].replace("'re", " are")
                doc[0] = doc[0].replace("'m", " am")
                doc[0] = doc[0].replace("n't", " not")
                for word in res.findall(doc[0]):
                    tmpWordLs.append(word)
                    doc[0] = doc[0].replace(word, '')
                for wordLs in res1.findall(doc[0]):
                    tmpWordLs.append(wordLs[0])
                    doc[0] = doc[0].replace(wordLs[0], '')
                for wordLs in res2.findall(doc[0]):
                    for word in wordLs:
                        if word != '':
                            tmpWordLs.append(word)
                            doc[0] = doc[0].replace(word, '')
                for word in res3.findall(doc[0]):
                    tmpWordLs.append(word)
                    doc[0] = doc[0].replace(word, '')

                raw = doc[0].lower()
                tokens = tokenizer.tokenize(raw)
                en_stop = get_stop_words("en")
                stopped_tokens = [i for i in tokens if i not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
                texts.extend(tmpWordLs)

                for word in texts:
                    if word.__len__() == 1:
                        print('test',word)
                        print(doc)
                        break
                e.write(json.dumps(texts)+'\n')

    """由于github上句子的特殊性，仅仅使用切割的方法，得到每个doc中的word"""
    @staticmethod
    def getDoc_set_Simple(trainCorpusSentence,testCorpusSentence,trainWord,testWord):
        deleteWord = ['<','>','>=','<=','-','+','*']

        reg = re.compile('([\w\_]+\(.*?\))')  ###取出函数
        reg1 = re.compile('[\r\n\"]')
        reg2 = re.compile('[\(\.\)]| - | \* |^- |^\* ')  ##去掉 (, ), .
        reg3 = re.compile(' +')
        reg4 = re.compile('^ ')
        reg5 = re.compile(r'(\w+\.\w+)')
        reg6 = re.compile(r'>=|<=|;|<|>|=|`|\[|\]|/|\"')
        reg7 = re.compile(r'(https?://[\w\.\-/]+)')
        reg8 = re.compile(r'((\w+\-)+\w+)')
        ###去除首部空格
        with open(trainWord,'w') as e:
            lineNumber = 0
            for doc in trainCorpusSentence:
                lineNumber += 1

                doc[0] = re.sub(reg1,' ',doc[0])   ## 去掉\r \n
                doc[0] = doc[0].strip('.')
                wordLs = []

                for word in reg.findall(doc[0]):   ##  取出函数
                    wordLs.append(word)
                    doc[0] = doc[0].replace(word,'')
                for word in reg7.findall(doc[0]):  ##  取出链接
                    wordLs.append(word)
                    doc[0] = doc[0].replace(word,'')
                for ls in reg8.findall(doc[0]):  ## 去除 www-wqww-ww
                    wordLs.append(ls[0])
                    doc[0] = doc[0].replace(ls[0], '')
                for word in reg5.findall(doc[0]):  ##  取出带小数点的数字
                    wordLs.append(word)
                    doc[0] = doc[0].replace(word,'')
                doc[0] = re.sub(reg2,' ', doc[0])
                doc[0] = re.sub(reg3,' ', doc[0])  ##去除空格
                doc[0] = re.sub(reg4,'', doc[0])  ##去除首部空格
                doc[0] = re.sub(reg6,'', doc[0])  ##去除首部空格

                doc[0] = doc[0].replace("'s"," is")
                doc[0] = doc[0].replace("'re"," are")
                doc[0] = doc[0].replace("'m"," am")
                doc[0] = doc[0].replace("n't"," not")
                doc[0] = doc[0].replace("(","")
                # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

                tmpWordLs = doc[0].lower().strip().split(' ')
                en_stop = get_stop_words("en")
                stopped_tokens = [word.strip(",:") for word in tmpWordLs if word not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
                texts.extend(wordLs)

                for word in texts:
                    if word.__len__() == 1:
                        texts.remove(word)

                e.write(json.dumps(texts)+'\n')
        reg = re.compile('([\w\_]+\(.*?\))')  ###取出函数
        reg1 = re.compile('[\r\n]')
        reg2 = re.compile('[\(\.\)]| - | \* |^- |^\* ')  ##去掉 (, ), .
        reg3 = re.compile(' +')
        reg4 = re.compile('^ ')
        reg5 = re.compile(r'(\w+\.\w+)')
        reg6 = re.compile(r'>=|<=|;|<|>|=|`|\[|\]|/')
        reg7 = re.compile(r'(https?://[\w\.\-/]+)')
        ###去除首部空格
        with open(testWord,'w') as e:
            lineNumber = 0
            for doc in testCorpusSentence:
                lineNumber += 1

                doc[0] = re.sub(reg1,' ',doc[0])   ## 去掉\r \n
                wordLs = []
                for word in reg.findall(doc[0]):   ##  取出函数
                    wordLs.append(word)
                    doc[0] = doc[0].replace(word,'')
                for word in reg7.findall(doc[0]):  ##  取出链接
                    wordLs.append(word.strip('.'))
                    doc[0] = doc[0].replace(word,'')

                for word in reg5.findall(doc[0]):  ##  取出带小数点的数字
                    wordLs.append(word)
                    doc[0] = doc[0].replace(word,'')
                doc[0] = re.sub(reg2,' ', doc[0])
                doc[0] = re.sub(reg3,' ', doc[0])  ##去除空格
                doc[0] = re.sub(reg4,'', doc[0])  ##去除首部空格
                doc[0] = re.sub(reg6,'', doc[0])  ##去除首部空格

                doc[0] = doc[0].replace("'s"," is")
                doc[0] = doc[0].replace("'re"," are")
                doc[0] = doc[0].replace("'m"," am")
                doc[0] = doc[0].replace("n't"," not")
                doc[0] = doc[0].replace("(","")
                # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

                tmpWordLs = doc[0].lower().strip().split(' ')
                en_stop = get_stop_words("en")
                stopped_tokens = [word.strip(",:") for word in tmpWordLs if word not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
                texts.extend(wordLs)

                for word in texts:
                    if word.__len__() == 1:
                        texts.remove(word)

                e.write(json.dumps(texts)+'\n')
    """由于github上句子的特殊性，仅仅使用切割的方法，得到每个doc中的word"""
    @staticmethod
    def getDoc_set_Second(trainCorpusSentence,testCorpusSentence,trainWord,testWord,respOwnerAndNameLs):
        deleteWord = ['<','>','>=','<=','-','+','*']

        reg1 = re.compile('[\r\n\"]')
        reg2 = re.compile(r'(https://github.com/'+respOwnerAndNameLs[0]+'/'+respOwnerAndNameLs[1]+'/pull/(\d+))')
        reg3 = re.compile(' +')
        reg4 = re.compile('^ ')
        # reg5 = re.compile('(`\w+`)')
        reg6 = re.compile('(`[\w\-\.\*/:]+`)')
        reg7 = re.compile('(```[\s\S]+?```)')
        reg8 = re.compile('(\.\.\.[\s\S]+?\.\.\.)')
        reg9 = re.compile('(<img[\s\S]+?>)')
        reg10 = re.compile(r'(https?://[\w\.\-/]+)')

        res = re.compile("[\[*\]*\)\(>;_\|*]")   ##消除word中的字符
        res2 = re.compile('^\d[\d.]+\d$')
        res3 = re.compile('\*|`|-|##+|\[|\]|&+|\?|~|/|!=|\.||\\\\')


        ###去除首部空格
        with open(trainWord,'w') as e:
            lineNumber = 0
            for doc in trainCorpusSentence:
                lineNumber += 1

                doc[0] = re.sub(reg7,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg6,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg8,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg9,'',doc[0])   ## 去掉图片

                doc[0] = re.sub(reg1,' ',doc[0])   ## 去掉\r \n
                doc[0] = doc[0].strip('.')
                wordLs = []

                for word in reg2.findall(doc[0]):  ##  取出链接
                    wordLs.append("#"+str(word[1]))
                    doc[0] = doc[0].replace(word[0],'')
                doc[0] = re.sub(reg10, '', doc[0])  ## 去掉链接

                doc[0] = re.sub(reg3,' ', doc[0])  ##去除空格
                doc[0] = re.sub(reg4,'', doc[0])  ##去除首部空格

                doc[0] = doc[0].replace("'s"," is")
                doc[0] = doc[0].replace("'re"," are")
                doc[0] = doc[0].replace("'m"," am")
                doc[0] = doc[0].replace("n't"," not")
                doc[0] = doc[0].replace("(","")
                # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

                tmpWordLs = doc[0].lower().strip().split(' ')
                en_stop = get_stop_words("en")
                stopped_tokens = [word.strip(",:.") for word in tmpWordLs if word not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
                texts.extend(wordLs)

                res_text = []
                for word in texts:

                    word = re.sub(res, '', word)
                    word = re.sub(res2, '', word)
                    word = re.sub(res3, '', word)
                    if word.__len__() > 1 and word not in en_stop:
                        res_text.append(word)

                e.write(json.dumps(res_text)+'\n')

        ###去除首部空格
        with open(testWord,'w') as e:
            lineNumber = 0
            for doc in testCorpusSentence:
                lineNumber += 1

                doc[0] = re.sub(reg7,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg6,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg8,'',doc[0])   ## 去掉代码
                doc[0] = re.sub(reg9,'',doc[0])   ## 去掉代码

                doc[0] = re.sub(reg1,' ',doc[0])   ## 去掉\r \n
                doc[0] = doc[0].strip('.')
                wordLs = []

                for word in reg2.findall(doc[0]):  ##  取出链接
                    wordLs.append("#"+str(word[1]))
                    doc[0] = doc[0].replace(word[0],'')

                doc[0] = re.sub(reg10, '', doc[0])  ## 去掉代码
                doc[0] = re.sub(reg3,' ', doc[0])  ##去除空格
                doc[0] = re.sub(reg4,'', doc[0])  ##去除首部空格

                doc[0] = doc[0].replace("'s"," is")
                doc[0] = doc[0].replace("'re"," are")
                doc[0] = doc[0].replace("'m"," am")
                doc[0] = doc[0].replace("n't"," not")
                doc[0] = doc[0].replace("(","")
                # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

                tmpWordLs = doc[0].lower().strip().split(' ')
                en_stop = get_stop_words("en")
                stopped_tokens = [word.strip(",:.") for word in tmpWordLs if word not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
                texts.extend(wordLs)

                res_text = []
                for word in texts:

                    word = re.sub(res, '', word)
                    word = re.sub(res2, '', word)
                    word = re.sub(res3, '', word)
                    if word.__len__() > 1 and word not in en_stop:
                        res_text.append(word)

                e.write(json.dumps(res_text)+'\n')

    """由于github上句子的特殊性，仅仅使用切割的方法，得到每个doc中的word"""
    @staticmethod
    def getDoc_set_First(trainCorpusSentence,testCorpusSentence,trainWord,testWord,respOwnerAndNameLs):
        deleteWord = ['<','>','>=','<=','-','+','*']

        reg1 = re.compile('[\r\n\"]')
        projectLink_reg = re.compile(r'(https://github.com/'+respOwnerAndNameLs[0]+'/'+respOwnerAndNameLs[1]+'/pull/(\d+))')
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

        res = re.compile("[\[*\]*\)\(>;_\|*]")   ##消除word中的字符
        res2 = re.compile('^\d[\d.]+\d$')
        res3 = re.compile('\*|`|-|##+|\[|\]|&+|\?|~|/|!=|\.|\\\\+|<+|=+')
        replaceStr = [u"“",u'–',u"”",u"→","(",u" ",u'🎵',u'©',u'😞',u'…',u"‘",u"’",u"²",u"⇒",u"฿",u"—",u"ł"]

        ###去除首部空格
        with open(trainWord,'w') as e:
            lineNumber = 0
            for doc in trainCorpusSentence:
                lineNumber += 1
                doc[0] = re.sub(img_reg,'',doc[0])   ## 去掉图片

                doc[0] = re.sub(reg1,' ',doc[0])   ## 去掉\r \n
                doc[0] = doc[0].strip('.')
                wordLs = []

                for word in projectLink_reg.findall(doc[0]):  ##  取出链接作为一个词
                    wordLs.append("#" + str(word[1]))
                    doc[0] = doc[0].replace(word[0], '')
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
                    doc[0] = doc[0].replace(word,'')

                doc[0] = re.sub(reg3,' ', doc[0])  ##去除空格
                doc[0] = re.sub(reg4,'', doc[0])  ##去除首部空格

                doc[0] = doc[0].replace(u"’s", " is")
                doc[0] = doc[0].replace("\u2019s", " is")
                doc[0] = doc[0].replace(u"’re", " are")
                doc[0] = doc[0].replace("\u2019re", " are")
                doc[0] = doc[0].replace(u"’m", " am")
                doc[0] = doc[0].replace("\u2019m", " am")
                doc[0] = doc[0].replace(u"n’t", " not")
                doc[0] = doc[0].replace("n\u2019t", " not")
                for val in replaceStr:
                    doc[0] = doc[0].replace(val,"")
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
                            word = word.replace(tmpStr, "")
                    word = re.sub(res, '', word)
                    word = re.sub(res2, '', word)
                    word = re.sub(res3, '', word)
                    if word.__len__() > 1 and word not in en_stop:
                        res_text.append(word)
                e.write(json.dumps(res_text)+'\n')

        ###去除首部空格
        with open(testWord, 'w') as e:
            lineNumber = 0
            for doc in testCorpusSentence:
                lineNumber += 1
                doc[0] = re.sub(img_reg, '', doc[0])  ## 去掉图片

                doc[0] = re.sub(reg1, ' ', doc[0])  ## 去掉\r \n
                doc[0] = doc[0].strip('.')
                wordLs = []

                for word in projectLink_reg.findall(doc[0]):  ##  取出链接作为一个词
                    wordLs.append("#" + str(word[1]))
                    doc[0] = doc[0].replace(word[0], '')
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
                    doc[0] = doc[0].replace(val,"")
                # doc[0] = doc[0].replace('[\(\)@\[\]\r\n]', '')

                tmpWordLs = doc[0].lower().strip().split(' ')
                en_stop = get_stop_words("en")
                stopped_tokens = [word.strip(",:.") for word in tmpWordLs if word not in en_stop]
                p_stemmer = PorterStemmer()
                texts = [p_stemmer.stem(word).encode('utf-8') for word in stopped_tokens]
                texts.extend(wordLs)

                res_text = []
                for word in texts:
                    word = word.replace(" ","")
                    if isinstance(word,unicode):
                        for tmpStr in replaceStr:
                            word = word.replace(tmpStr, "")
                    word = re.sub(res, '', word)
                    word = re.sub(res2, '', word)
                    word = re.sub(res3, '', word)
                    if word.__len__() > 1 and word not in en_stop:
                        res_text.append(word)
                e.write(json.dumps(res_text) + '\n')

def mergeTrainAndTest(trainWord,testWord,outfilepath):
    with open(outfilepath,'w') as e:
        with open(trainWord,'r') as e1:
            for line in e1:
                e.write(line)
        with open(testWord,'r') as e2:
            for line in e2:
                e.write(line)

def getRespNameAndOwner(projectNameFile):
    with open(projectNameFile,'r') as e:
        for line in e:
            return json.loads(line)

if __name__ == '__main__':
    # basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的CNN实验(过滤训练集标签) /'
    #basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(5个月)/'
    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    parameter = 2000
    projectDict = smallCorpusTrain.computePRofTestCorpusNumber(parameter)
    print(projectDict)
    for projectName in projectDict:
        if parameter == 4000 and projectName in ['bitcoin']: ###第一个训练集的数目选择4000时,bitcoin将会没有测试集
            continue
        projectFile = projectName + '项目实验/'
        projectNameFile = unicode(basicFilepath+projectFile+'项目名.txt','utf-8')
        respOwnerAndNameLs = getRespNameAndOwner(projectNameFile)
        print(respOwnerAndNameLs)
        for i in xrange(1, projectDict[projectName] + 1):
            trainNumberFile = '第' + str(i) + '次训练/'
            trainBasicFile = basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
            testBasicFile = basicFilepath + projectFile + trainNumberFile + 'testCorpus/'
            newTrainCorpus = unicode(trainBasicFile +str(parameter)+'trainCorpus.txt', 'utf-8')
            # trainWord = unicode(trainBasicFile + 'second_trainCorpus_word.txt', 'utf-8')
            trainWord = unicode(trainBasicFile +str(parameter)+'_1_trainCorpus_word.txt', 'utf-8')
            print(trainWord)
            newTestCorpus = unicode(testBasicFile +str(parameter)+'testCorpus.txt', 'utf-8')
            # testWord = unicode(testBasicFile + 'second_testCorpus_word.txt', 'utf-8')
            testWord = unicode(testBasicFile +str(parameter)+'_1_testCorpus_word.txt', 'utf-8')

            trainCorpusSentence = Corpus(newTrainCorpus)
            testCorpusSentence = Corpus(newTestCorpus)

            # TokenWord.getDoc_set_Second(trainCorpusSentence,testCorpusSentence,trainWord,testWord,respOwnerAndNameLs)
            TokenWord.getDoc_set_First(trainCorpusSentence,testCorpusSentence,trainWord,testWord,respOwnerAndNameLs)