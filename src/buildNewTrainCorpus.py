#coding=utf-8

"""

第一步：过滤出现次数小于50次的tag
并构建新的数据集
"""

import json
from handleCorpus import *
from projectSelect.smallcorpusTrain import smallCorpusTrain

class buildNewCorpus():
    trainCorpus_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1\trainCorpus.txt'
    middleResul_filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1'
    tmpPath = r'\exper1'
    tagFilepath = middleResul_filepath+tmpPath+r'\filterTagsNum.txt' ###去掉了出现次数少于50次的tag文件
    afterFilterObjectTagFilepath =  middleResul_filepath+tmpPath+r'\atferFilterObjectTag.txt'

    """得到出现次数大于等于50次的tag,并分别得到训练集和测试集的tag"""
    @staticmethod
    def getTagMoreThan50(trainCorpus,testCorpus,trainTagFile,testTagFile,tagLessthan):
        tagNumberDict = {}
        with open(trainTagFile,'w') as e1:
            with open(trainCorpus,'r') as e:
                for line in e:
                    data = json.loads(line)
                    tmpLs = data["labelName"].strip(',').split(',')
                    for tag in tmpLs:
                        tagNumberDict[tag] = tagNumberDict.get(tag,0)+1
                    e1.write(json.dumps(tmpLs)+'\n')
        with open(testTagFile, 'w') as e1:
            with open(testCorpus,'r') as e:
                for line in e:
                    data = json.loads(line)
                    tmpLs = data["labelName"].strip(',').split(',')
                    for tag in tmpLs:
                        tagNumberDict[tag] = tagNumberDict.get(tag,0)+1
                    e1.write(json.dumps(tmpLs) + '\n')
        # print(tagNumberDict)
        # print len(dict(filter(lambda x:x[1]<tagLessthan,tagNumberDict.items())).keys())
        return dict(filter(lambda x:x[1]>=tagLessthan,tagNumberDict.items())).keys()

    """删除出现次数小于50次的tag，并得到无tag的数据"""
    @staticmethod
    def filterTagLessThan50(trainTagFile,testTagFile,newTrainTagFile,newTestTagFile,tagLs):
        deleteTag = []
        trainNotTagLineLs = []
        testNotTagLineLs = []
        with open(newTrainTagFile,'w') as e:
            with open(trainTagFile,'r') as e1:
                lineNum = 0
                for line in e1:
                    lineNum +=1
                    data = json.loads(line)
                    tmpLs = [tag for tag in data if tag in tagLs]
                    deleteTag = [tag for tag in data if tag not in tagLs]
                    if tmpLs.__len__() == 0:
                        trainNotTagLineLs.append(lineNum)
                    else:
                        e.write(json.dumps(tmpLs) + '\n')
        with open(newTestTagFile,'w') as e:
            with open(testTagFile,'r') as e1:
                lineNum = 0
                for line in e1:
                    lineNum +=1
                    data = json.loads(line)
                    tmpLs = [tag for tag in data if tag in tagLs]
                    if tmpLs.__len__() == 0:
                        testNotTagLineLs.append(lineNum)
                    else:
                        e.write(json.dumps(tmpLs) + '\n')
        return trainNotTagLineLs,testNotTagLineLs,deleteTag

    """新建训练集和测试集"""
    @staticmethod
    def generateNewCorpus(trainCorpus,testCorpus,newTrainCorpus,newTestCorpus,trainNotTagLineLs,testNotTagLineLs):
        with open(newTrainCorpus,'w') as e:
            with open(trainCorpus,'r') as e1:
                lineNum = 0
                for line in e1:
                    lineNum+=1
                    if lineNum in trainNotTagLineLs:
                        continue
                    tmpLs = []
                    data = json.loads(line)
                    if data.get("body") != None:
                        tmpLs.append('#' + str(data['number']) + " "+data.get("body") + " " + data.get("title"))
                    else:
                        tmpLs.append('#' + str(data['number']) + " "+data.get("title"))
                    e.write(json.dumps(tmpLs)+'\n')
                    # data = json.loads(line)
                    # if data.get("body") != None:
                    #     reStr = u'#' + unicode(str(data['number']),'utf-8') + u" " + data.get("body") + u" " + data.get("title")
                    # else:
                    #     reStr = u'#' + unicode(str(data['number']),'utf-8') + u" " + data.get("title")
                    # e.write(reStr.encode('utf-8') + '\n')

        with open(newTestCorpus,'w') as e:
            with open(testCorpus,'r') as e1:
                lineNum = 0
                for line in e1:
                    lineNum+=1
                    if lineNum in testNotTagLineLs:
                        continue
                    tmpLs = []
                    data = json.loads(line)
                    if data.get("body") != None:
                        tmpLs.append('#' + str(data['number']) + " "+data.get("body") + " " + data.get("title"))
                    else:
                        tmpLs.append('#' + str(data['number']) + " "+data.get("title"))
                    e.write(json.dumps(tmpLs)+'\n')

                    # data = json.loads(line)
                    # if data.get("body") != None:
                    #     reStr = u'#' + unicode(str(data['number']),'utf-8') + u" " + data.get("body") + u" " + data.get("title")
                    # else:
                    #     reStr = u'#' + unicode(str(data['number']),'utf-8') + u" " + data.get("title")
                    # e.write(reStr.encode('utf-8')+'\n')


if __name__ == '__main__':

    # basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验/'
    #basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(5个月)/'
    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    # basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的CNN实验(过滤训练集标签) /'
    # projectDict = {'angular':45,'bitcoin':67,'elasticsearch':40,'owncloud':39,'pydata':40,'rails':64,'RIOT-OS':39,'symfony':70,'tgstation':30,'ceph':7}
    parameter = 2000
    projectDict = smallCorpusTrain.computePRofTestCorpusNumber(parameter)
    print(projectDict)
    for projectName in projectDict:
        if parameter >= 4000 and projectName in ['bitcoin']: ###第一个训练集的数目选择4000时,bitcoin将会没有测试集
            continue
        projectFile = projectName+'项目实验/'
        for i in xrange(1,projectDict[projectName]+1):
            trainNumberFile = '第'+str(i)+'次训练/'
            trainBasicFile = basicFilepath+projectFile+trainNumberFile+'trainCorpus/'
            testBasicFile = basicFilepath+projectFile+trainNumberFile+'testCorpus/'
            trainCorpus = unicode(trainBasicFile+str(parameter)+'训练集.txt','utf-8')
            testCorpus = unicode(testBasicFile+str(parameter)+'测试集.txt','utf-8')
            newTrainCorpus = unicode(trainBasicFile+str(parameter)+'trainCorpus.txt','utf-8')
            newTestCorpus = unicode(testBasicFile+str(parameter)+'testCorpus.txt','utf-8')
            trainTagFile = unicode(trainBasicFile+str(parameter)+'标签.txt','utf-8')
            newTrainTagFile = unicode(trainBasicFile+str(parameter)+'tag.txt','utf-8')
            testTagFile = unicode(testBasicFile+str(parameter)+'标签.txt','utf-8')
            newTestTagFile = unicode(testBasicFile+str(parameter)+'tag.txt','utf-8')
            # print trainTagFile
            # print(trainCorpus)
            # print(testCorpus)
            tagLs = buildNewCorpus.getTagMoreThan50(trainCorpus,testCorpus,trainTagFile,testTagFile,tagLessthan=0)
            trainNotTagLineLs, testNotTagLineLs,deleTag = buildNewCorpus.filterTagLessThan50(trainTagFile,testTagFile,newTrainTagFile,newTestTagFile,tagLs)
            # print trainNotTagLineLs.__len__()
            # print testNotTagLineLs.__len__()
            print({projectName+'_'+str(i):deleTag})

            buildNewCorpus.generateNewCorpus(trainCorpus, testCorpus, newTrainCorpus, newTestCorpus, trainNotTagLineLs, testNotTagLineLs)

