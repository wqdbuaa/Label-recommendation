#coding=utf-8

from dateCompare import *
import json
from smallcorpusTrain import *
import pandas as pd

"""抽取最后一个月的tag"""
def extractLastMonthTag(corpusFile, prNumberLs, tagfile):
    tagDict = {}
    with open(tagfile,'w') as e1:
        with open(corpusFile,'r') as e:
            for line in e:
                data = json.loads(line)
                if data['number'] in prNumberLs:
                    tagLs = data["labelName"].strip(',').split(',')
                    for tag in tagLs:
                        tagDict[tag] = tagDict.get(tag,0)+1
        tagLs = sorted(tagDict.items(), key=lambda x: x[1], reverse=True)
        for tmpLs in tagLs:
            e1.write(json.dumps(tmpLs) + '\n')

"""抽取测试集的tag"""
def extractTestTag(corpusFile, tagfile):
    tagDict = {}
    with open(tagfile,'w') as e1:
        with open(corpusFile,'r') as e:
            for line in e:
                data = json.loads(line)
                tagLs = data["labelName"].strip(',').split(',')
                for tag in tagLs:
                    tagDict[tag] = tagDict.get(tag,0)+1
        tagLs = sorted(tagDict.items(),key=lambda x:x[1],reverse=True)
        for tmpLs in tagLs:
            e1.write(json.dumps(tmpLs)+'\n')

"""训练集的第一条是最近的一条pull request"""
def extractPRNumber(corpus):
    prNumberLs = []
    with open(corpus, 'r') as e:
        for line in e:
            data = json.loads(line)
            # print(data['number'])
            endTime = data['created_at']
            break
    startTime = dateCompare.timeSumMonth(endTime,-1)
    # print(endTime)
    # print(startTime)
    with open(corpus, 'r') as e:
        for line in e:
            data = json.loads(line)
            if dateCompare.dateCompareto(data['created_at'],startTime,2):  ##创建时间小于startTime
                # print(data['number'])
                break
            else:
                prNumberLs.append(data['number'])
    return prNumberLs

"""写lastMonthTag.csv"""
def writeLastMonthTagCsv(BPtagCSV,lastmonthTag,lastmonthTagCSV):
    BPTagDF = pd.read_csv(BPtagCSV)
    tagColumns = BPTagDF.columns
    with open(lastmonthTagCSV,'w') as e:
        e.write(",".join(tagColumns) + '\n')
        with open(lastmonthTag,'r') as e1:
            for line in e1:
                data = json.loads(line)
                tmpLs = []
                for val in tagColumns:
                    if val in data:
                        tmpLs.append('1')
                    else:
                        tmpLs.append('0')
                e.write(",".join(tmpLs)+'\n')

"""检查不同的tag"""
def checkDifferentTag(testTag,lastTag,trainTag):
    testTagSet = set()
    lastTagSet = set()
    trainTagSet = set()
    with open(testTag,'r') as e:
        for line in e:
            data = json.loads(line)
            testTagSet.add(data[0])
    with open(lastTag,'r') as e:
        for line in e:
            data = json.loads(line)
            lastTagSet.add(data[0])
    with open(trainTag,'r') as e:
        for line in e:
            data = json.loads(line)
            trainTagSet.add(data[0])
    print(lastTagSet.difference(testTagSet))
    print(testTagSet.difference(lastTagSet))
    print(testTagSet.difference(trainTagSet))

"""抽取每个tag被最后一次使用的pull requets的number"""
def extractTagNumber(corpusFile,tag_PRNumberFile):
    tagDict = {}
    tmpDict = {}
    with open(tag_PRNumberFile, 'w') as e1:
        with open(corpusFile, 'r') as e:
            for line in e:
                data = json.loads(line)
                tagLs = data["labelName"].strip(',').split(',')
                for tag in tagLs:
                    if tag not in tagDict:
                        tagDict[tag] = []
                    tagDict[tag].append(data['number'])
        for tag in tagDict:
            tmpDict[tag] = max(tagDict[tag])
        for ls in sorted(tmpDict.items(),key=lambda x:x[1],reverse=True):
            e1.write(json.dumps(ls)+'\n')

if __name__ == '__main__':
    """第一步: 推荐标签"""
    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    projectDict = smallCorpusTrain.computePRofTestCorpusNumber()
    print(projectDict)
    for projectName in projectDict:
        if projectName != 'elasticsearch':
            continue
        projectFile = projectName + '项目实验/'
        for i in xrange(1, projectDict[projectName] + 1):
        # for i in xrange(1, 2):

            trainNumberFile = '第' + str(i) + '次训练/'
            trainBasicFile = basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
            testBasicFile = basicFilepath + projectFile + trainNumberFile + 'testCorpus/'

            trainCorpus = unicode(trainBasicFile+'训练集.txt','utf-8')
            testCorpus = unicode(testBasicFile+'测试集.txt','utf-8')

            testTag = unicode(trainBasicFile+'testTag.txt','utf-8')
            trainTag = unicode(trainBasicFile+'trainTag.txt','utf-8')
            lastMonthTag = unicode(trainBasicFile+'lastMonthTag.txt','utf-8')
            lastUseTag_prNumber = unicode(trainBasicFile+'lastUseTag_prNumber.txt','utf-8')
            lastmonthTagCSV = unicode(trainBasicFile+'lastMonthTag.csv','utf-8')
            BPtagCSV = unicode(trainBasicFile+'BPtag.csv','utf-8')

            """得到最近一个月的pr的number"""
            prNumberLs = extractPRNumber(trainCorpus)
            print(prNumberLs.__len__())
            """得到最近一个月的常用tag"""
            extractLastMonthTag(trainCorpus,prNumberLs,lastMonthTag)

            """得到每个tag最后一次使用的pr的Number"""
            # extractTagNumber(trainCorpus, lastUseTag_prNumber)


            """观察训练集和测试集，最后一个数据集的不同tag"""
            # extractTestTag(testCorpus,testTag)  ##抽取测试集的tag
            # extractTestTag(trainCorpus,trainTag)  ##抽取测试集的tag
            # checkDifferentTag(testTag,lastMonthTag,trainTag)
            # """将tag写入csv中"""
            # writeLastMonthTagCsv(BPtagCSV, lastMonthTag, lastmonthTagCSV)

