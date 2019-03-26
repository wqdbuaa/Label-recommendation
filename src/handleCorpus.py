# coding=utf-8
'''
Created on 2017年5月7日

@author: Administrator
'''

import json
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words


class getCorpus():
    #     testCorpus_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\testProgrammer\testCorpus.txt'
    #     trainCorpus_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\testProgrammer\trainCorpus.txt'
    #     middleResul_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\testProgrammer/'

    testCorpus_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1\testCorpus.txt'
    trainCorpus_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1\trainCorpus.txt'
    middleResul_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1'
    tmpPath = r'\exper1'
    middleResul_filepath += tmpPath
    trainPRTag_filepath = middleResul_filepath+'\prTag.txt'

    corpus_doc = []  ##所有文章
    doc_set = []  ##二维数组，每一行表示一篇文章的词语
    doc_object = []  ##语料的字典
    object_tag = []

    """
    读取爬取的pull request中title 和 body
    """

    @staticmethod
    def readFile(filepath):
        with open(filepath, 'r') as e:

            for line in e:
                data = json.loads(line)
                if data.get("body") == None:
                    getCorpus.corpus_doc.append(data.get("title"))
                else:
                    getCorpus.corpus_doc.append(data.get("body") + unicode(" ", "utf-8") + data.get("title"))

    """
    得到每个doc中的word
    """

    @staticmethod
    def getDoc_set():
        tokenizer = RegexpTokenizer(r'\w+')
        for doc in getCorpus.corpus_doc:
            #             print type(doc)
            raw = doc.lower()
            tokens = tokenizer.tokenize(raw)
            en_stop = get_stop_words("en")
            stopped_tokens = [i for i in tokens if i not in en_stop]
            p_stemmer = PorterStemmer()
            texts = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
            getCorpus.doc_set.append(texts)

    @staticmethod
    def getNew_object(docs, newDoc_object):
        tokenizer = RegexpTokenizer(r'\w+')
        for doc in docs:
            #             print type(doc[1])
            raw = doc[1].lower()
            tokens = tokenizer.tokenize(raw)
            en_stop = get_stop_words("en")
            stopped_tokens = [i for i in tokens if i not in en_stop]
            p_stemmer = PorterStemmer()
            texts = {}
            #             texts = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
            #             print texts
            for i in stopped_tokens:
                texts[p_stemmer.stem(i).encode('utf-8')] = texts.get(p_stemmer.stem(i).encode('utf-8'), 0) + 1
            newDoc_object.append(texts)

    """
        返回待推荐的doc
    """

    @staticmethod
    def getNew_doc(filepath):
        new_doc = []
        with open(filepath, 'r') as e:
            for line in e:
                data = json.loads(line)
                tmpDoc = []
                tmpDoc.append(data.get("number"))
                if data.get("body") == None:
                    tmpDoc.append(data.get("title"))
                else:
                    tmpDoc.append(data.get("body") + unicode(" ", "utf-8") + data.get("title"))
                new_doc.append(tmpDoc)
        return new_doc

    """
    统计doc包含每种word的个数
    """

    @staticmethod
    def getDoc_object():
        objectDict = {}
        for doc in getCorpus.doc_set:
            for word in doc:
                objectDict[word] = objectDict.get(word, 0) + 1
            getCorpus.doc_object.append(objectDict)

    """
    保存结果
    """

    @staticmethod
    def saveResult(filepath):
        filepath1 = filepath + r'\dictionary.txt'
        with open(filepath1, 'w') as e:
            e.write(json.dumps(getCorpus.doc_object[0]))
            e.flush()

        filepath2 = filepath + r'\doc_word.txt'
        with open(filepath2, 'w') as e:
            for line in getCorpus.doc_set:
                e.write(json.dumps(line) + '\n')
            e.flush()

    """
    得到pr的所有tag，并写入文件
    """
    @staticmethod
    def getObjectTag(filepath):
        with open(filepath, 'r') as e:
            for line in e:
                tmpDict = []
                data = json.loads(line)
                # print data
                tmpDict.append(data["owner"])
                tmpDict.append(data["respName"])
                tmpDict.append(data["number"])
                tmpDict.extend(data["labelName"].strip(',').split(','))
                getCorpus.object_tag.append(tmpDict)

    """得到出现次数小于50的tag"""
    @staticmethod
    def getTagNumOfCorpusLessThan(tagLessthan=50):
        # objectTag = getCorpus.getObjectTag(sourceFilepath)
        # print objectTag
        tagDict = {}
        for ls in getCorpus.object_tag:
            for tag in ls[3:]:
                    tagDict[tag] = tagDict.get(tag,0)+1

        retTagList = dict(filter(lambda x:x[1]<tagLessthan,tagDict.items())).keys() ###记录出现次数小于50的tag
        return retTagList

    """从文件中读取出现次数小于50的tag"""
    @staticmethod
    def readTagLessthan(filepath):
        tagList = []
        with open(filepath,'r') as e:
            for line in e:
                tagList = json.loads(line)
        return tagList

    """
    将pr的tag数目写入destinationFilepath
    将pr的出现次数大于5的tag写入filterTagFilepath
    """
    @staticmethod
    def writeTagNumOfCorpusToFile(destinationFilepath, filterTagFilepath,lessthanTagFilepath,tagLessthan=50):
        # objectTag = getCorpus.getObjectTag(sourceFilepath)
        # print objectTag
        tagDict = {}
        with open(destinationFilepath, 'w') as e:
            for ls in getCorpus.object_tag:
                for tag in ls[3:]:
                    tagDict[tag] = tagDict.get(tag, 0) + 1
            for key in tagDict:
                e.write(key+','+str(tagDict[key]) + '\n')
                e.flush()
        """保存出现次数大于50次的tag """
        with open(filterTagFilepath, 'w') as e:
            # for key in tagDict:
            #     if tagDict[key]<50:
            #         tagDict.popitem()
            newDict = dict(filter(lambda x: x[1] >= tagLessthan, tagDict.items()))
            for key in newDict:
                e.write(json.dumps([key,newDict[key]]) + '\n')
                e.flush()
        """保存出现次数低于50次的tag """
        with open(lessthanTagFilepath, 'w') as e:
            # for key in tagDict:
            #     if tagDict[key]<50:
            #         tagDict.popitem()
            newLs = dict(filter(lambda x: x[1] < tagLessthan, tagDict.items())).keys()

            e.write(json.dumps(newLs) + '\n')
            e.flush()

if __name__ == '__main__':
    #     filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus\trainCorpus.txt'
    #     filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\testProgrammer\trainCorpus.txt'

    getCorpus.readFile(getCorpus.trainCorpus_filepath)
    getCorpus.getDoc_set()
    getCorpus.getDoc_object()
    # #     for i in range(len(getCorpus.doc_set)
    getCorpus.getObjectTag(getCorpus.trainCorpus_filepath)
    print getCorpus.getTagNumOfCorpusLessThan()