#coding=utf-8

from handleCorpus import *
from buildNewTrainCorpus import *
from dataHandle import *

class filepath:

    trainCorpus = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\trainCorpus\含有10000条数据的训练集.txt',
                          'utf-8')
    testCorpus = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\testCorpus\以3个月为时间节点的测试集.txt',
                          'utf-8')

    newTrainCorpus = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\trainCorpus\过滤tag出现次数较低后得到的训练集.txt',
                          'utf-8')

    tagFile = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\中间过程\未筛选前训练集所有的tag.txt',
                      'utf-8')
    tagMorethan50_File = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\中间过程\出现次数大于等于50的tag.txt',
                      'utf-8')
    tagLessthan50_File = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\中间过程\出现次数低于50的tag.txt',
                          'utf-8')

    """为pull request的number与index建立索引"""
    prNumberToIndex = unicode(r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpusStatistic\待推荐的小数目项目进行实验\trainCorpus\训练集prNumber与index的索引.txt',
                          'utf-8')

if __name__ == '__main__':
    getCorpus.getObjectTag(filepath.trainCorpus)
    print getCorpus.getTagNumOfCorpusLessThan()
    """将训练中所有tag写入文件，并记录出现次数大于20次的tag"""
    getCorpus.writeTagNumOfCorpusToFile(filepath.tagFile,filepath.tagMorethan50_File,filepath.tagLessthan50_File,20)
    removeTagList = getCorpus.readTagLessthan(filepath.tagLessthan50_File)
    buildNewCorpus.buildNewCorpus(filepath.trainCorpus,filepath.newTrainCorpus,removeTagList)

    """为pull request的number与index建立索引"""
    dataHandle.saveNumbertoFile(filepath.newTrainCorpus,filepath.prNumberToIndex)