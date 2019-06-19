#coding=utf-8

import torch
from torch.autograd import Variable
import torch.nn.functional as F

import pandas as pd
import numpy as np
from collections import OrderedDict
from torch.nn.parameter import Parameter
from fileConfig.filepath import filepathConfig
from xlwt import Workbook
from xlutils.copy import copy
import xlrd
import os
import time,json,math,datetime
from time import time

"""建立权重矩阵"""
def buildWeightMatrix(lastMonthTag,BPTagCsv,outCsv):
    tagDict = {}
    BP_DF = pd.read_csv(BPTagCsv)
    tagColumns = BP_DF.columns
    with open(lastMonthTag,'r') as e:
        for line in e:
            data = json.loads(line)
            tagDict[data[0]] = data[1]

    tagCount = sum(tagDict.values())
    for tag in tagDict:
        tagDict[tag] = tagDict[tag]/ float(tagCount)
    # print(tagDict)
    lineIndex = 0
    with open(outCsv,'w') as e1:
        with open(BPTagCsv,'r') as e:
            for line in e:
                if lineIndex == 0:
                    e1.write(line)
                    lineIndex+=1
                    continue
                data = line.strip().split(',')
                assert  data.__len__() == tagColumns.__len__()
                for i in xrange(tagColumns.__len__()):
                    if data[i] == '1' and tagColumns[i] in tagDict:
                        data[i] = str(1+tagDict[tagColumns[i]])
                e1.write(",".join(data)+'\n')
    return pd.read_csv(outCsv)

"""利用label co-occurence建立权重矩阵"""
def buildWeightMatrixByLabel_cooccurence(lastMonthTag,BPTagCsv,trainTag,linkCreateTagOccurrenceNumber,hiddenNumber,outputNumber,outCsv):
    # lastMonthTagDict = {}
    # with open(lastMonthTag,'r') as e:
    #     for line in e:
    #         data = json.loads(line)
    #         lastMonthTagDict[data[0]] = data[1]
    # tagSumCount = sum(lastMonthTagDict.values())

    BP_DF = pd.read_csv(BPTagCsv)
    tagColumns = BP_DF.columns.tolist()
    tagDict = {}
    with open(trainTag,'r') as e:
        for line in e:
            data = json.loads(line)
            if data.__len__() == 1:
                continue
            tagStr = ",".join(data)
            tagDict[tagStr] = tagDict.get(tagStr,0)+1
    # print(linkCreateTagOccurrenceNumber)
    with open(linkCreateTagOccurrenceNumber,'r') as e:
        for line in e:
            data = json.loads(line)
            if data.__len__() == 1:
                continue
            tagStr = ",".join(data)
            tagDict[tagStr] = tagDict.get(tagStr,0)+1
    tmpValue = math.sqrt(6)/math.sqrt(hiddenNumber+outputNumber)
    # print(tagDict.__len__())

    with open(outCsv,'w') as e:
        e.write(",".join(tagColumns)+'\n')
        for tagStr in tagDict:
            tmpLs = []
            data = tagStr.split(',')
            for tag in tagColumns:
                if tag in data:
                    # if tag in lastMonthTagDict:
                    #
                    #     tmpLs.append(str(tagDict[tagStr]*tmpValue+lastMonthTagDict[tag]/float(tagSumCount)))
                    # else:
                    tmpLs.append(str(tagDict[tagStr] * tmpValue))
                else:
                    tmpLs.append('0')
            e.write(",".join(tmpLs)+'\n')
    return pd.read_csv(outCsv)


def computePrecession(netOut,y,topLs):
    precessionLs = []
    recallLs = []
    F1Ls = []

    pred_y = netOut.data.numpy()
    actu_y = y.data.numpy()
    length = pred_y.shape[0]

    print(pred_y.shape)
    print(actu_y.shape)
    assert pred_y.shape==actu_y.shape

    resDict = {}
    for topNumber in topLs:
        for i in xrange(length):
            count = 0
            pred_tag = []
            actu_tag = actu_y[i]
            tmpLs1 = pred_y[i]
            tmpLs2 = pred_y[i]
            tmpVal = sorted(tmpLs2)[-topNumber]
            j = 0
            for val in tmpLs1:
                if val > tmpVal:
                    pred_tag.append(1)
                else:
                    if val == tmpVal:
                        final_j = j
                    pred_tag.append(0)
                j += 1
            pred_tag[final_j] = 1

            for index in xrange(pred_tag.__len__()):
                if pred_tag[index] == 1 and actu_tag[index] == pred_tag[index]:
                    count +=1
            precessionLs.append(float(count)/topNumber)
            recallLs.append(float(count)/sum(actu_tag))
            # if sum(actu_tag)<=topNumber:
            #     recallLs.append(float(count)/sum(actu_tag))
            # else:
            #     recallLs.append(float(count)/topNumber)

            # print(tmpLs1)
            # print(sorted(tmpLs2)[-topNumber])
            # print(pred_tag)
            # print(actu_tag)
            # print(precessionLs)
            # break
            # if precessionLs.__len__() == recallLs.__len__():
            #     print(True)
        for index in xrange(len(precessionLs)):
            if recallLs[index] + precessionLs[index] == 0:
                F1Ls.append(0.0)
            else:
                F1Ls.append(2*(recallLs[index] * precessionLs[index])/(recallLs[index] + precessionLs[index]))
        resDict[topNumber] = [sum(precessionLs)/precessionLs.__len__(),sum(recallLs)/recallLs.__len__(),sum(F1Ls)/F1Ls.__len__()]
    return resDict

def writeRecommendTag(recommedTag,actualTag,outpath,timeCosumingFile,trainTime,predictTime):

    pred_y = recommedTag.data.numpy()
    tagLs = actualTag.columns.tolist()
    with open(timeCosumingFile,'w') as e:
        e.write(json.dumps([trainTime,predictTime])+'\n')

    with open(outpath,'w') as e:
        for i in xrange(pred_y.__len__()):
            tmpDict = {key:value for key,value in enumerate(pred_y[i])}
            tmpTuple = sorted(tmpDict.items(),key=lambda x:x[1],reverse=True)
            pred_Tag = [tagLs[ls[0]] for ls in tmpTuple]
            # print(pred_Tag)
            e.write(json.dumps(pred_Tag)+'\n')

def computePRofTestCorpusNumber(originPath,parameter=3000):
    resDict = {}
    retLs = []
    for tmpstr in ['angular','bitcoin','elasticsearch','owncloud','pydata','rails','RIOT-OS','symfony','tgstation','ceph']:
        # if parameter == 3000:
        #     splitProject = unicode(originPath + tmpstr + r'项目实验/项目集划分.txt', 'utf-8')
        # else:
        splitProject = unicode(originPath + tmpstr + r'项目实验/' + str(parameter) + '项目集划分.txt', 'utf-8')
        print(splitProject)
        with open(splitProject, 'r') as e:  ## 从项目集划分中读出项目的划分情况
            for line in e:
                retLs = json.loads(line)
        resDict[tmpstr] = retLs.__len__()
    return resDict

if __name__ == '__main__':

    parameter = 2000 ###"""第一个训练集文本数量"""
    hiddenNeurons = 1
    epoch = 40

    learning_rate = 0.005
    originPath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    #originPath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(1个月)/'


    """月份调节"""
    projectIndex = {'symfony':7,'tgstation':5,'pydata':1,'bitcoin':2,'rails':7,'ceph':6,'owncloud':1,'elasticsearch':4,'angular':1,'RIOT-OS':7}
    projectIndex = {'symfony':7,'tgstation':4,'pydata':1,'bitcoin':2,'rails':7,'ceph':5,'owncloud':1,'elasticsearch':2,'angular':1,'RIOT-OS':7}
    projectDict = computePRofTestCorpusNumber(originPath,parameter)
    print(projectDict)
    for epoch in [40]:
        print str(epoch)+'-----------------------------------'
        for projectName in projectDict:
            # if projectName != 'tgstation':
            #     continue

            if projectName == 'bitcoin' and parameter == 4000:
                continue
            projectFile = projectName + '项目实验/'

            try:

               for i in xrange(projectIndex[projectName], projectDict[projectName]+1):
               #for i in xrange(1, projectDict[projectName]+1):
                    #if i != 3:
                    #    continue
                    cudaFlag = False
                    #cudaFlag = True

                    fp = filepathConfig(projectName,i,hiddenNeurons,epoch = epoch,learning_rate = learning_rate,parameter = parameter)
                    print(fp.trainTag_csv)
                    topLs = [1,2,3,4,5,10]
                    xDF = pd.read_csv(fp.doc2bow_train)
                    yDF = pd.read_csv(fp.trainTag_csv)
                    xNumpy = xDF.values
                    # print xNumpy.shape
                    # print yDF.shape
                    x,y= Variable(torch.FloatTensor(xNumpy)),Variable(torch.FloatTensor(yDF.values))
                    print(u"输入x:") ###0表示样本个数，1表示神经元个数trainCorpus
                    print(x.size()) ###0表示样本个数，1表示神经元个数
                    print(u"输出y:")
                    print(y.size())

                    inputCellNumber = x.size()[1]
                    outputCellNumber = y.size()[1]
                    hiddenCellNumber1 = int(inputCellNumber * hiddenNeurons)
                    hiddenCellNumber2 = int(inputCellNumber * hiddenNeurons)
                    hiddenCellNumber3 = int(inputCellNumber * hiddenNeurons)

                    # nn.Sequential(OrderedDict([
                    #                   ('conv1', nn.Conv2d(1,20,5)),
                    #                   ('relu1', nn.ReLU()),
                    #                   ('conv2', nn.Conv2d(20,64,5)),
                    #                   ('relu2', nn.ReLU())
                    #                 ]))

                    class Net(torch.nn.Module):
                        def __init__(self,n_features,n_hidden1,n_hidden2,n_hidden3,n_output):
                        # def __init__(self,n_features,n_hidden1,n_output):
                            super(Net,self).__init__()
                            self.hidden1 = torch.nn.Linear(n_features,n_hidden1)
                            # self.hidden2 = torch.nn.Linear(n_hidden1,n_hidden2)
                            # self.hidden3 = torch.nn.Linear(n_hidden2,n_hidden3)
                            torch.nn.Dropout(0.5)
                            self.predict = torch.nn.Linear(n_hidden1,n_output)

                        def forward(self, x):
                            x = F.relu(self.hidden1(x))
                            # x = F.relu(self.hidden2(x))
                            # x = F.relu(self.hidden3(x))
                            x = self.predict(x)
                            return x

                    # BPnet = torch.nn.Sequential(OrderedDict([
                    #     ('line1',torch.nn.Linear(5174,6500)),
                    #     ('sigmoid',torch.nn.LogSigmoid()),
                    #     ('line2',torch.nn.Linear(6500,64))]))
                    # BPnet = Net(5174,6318,64) ##symfony
                    # BPnet = Net(5218,6038,28)   ##rails
                    BPnet = Net(inputCellNumber,hiddenCellNumber1,hiddenCellNumber2,hiddenCellNumber3,outputCellNumber)   ##添加三个隐藏层
                    # BPnet = Net(inputCellNumber,hiddenCellNumber1,outputCellNumber)   ##ceph
                    # BPnet = Net(inputCellNumber,hiddenCellNumber1,outputCellNumber)   ##ceph
                    # print(u"隐藏层到输出层权重矩阵")
                    # print(BPnet.predict.weight.size())

                    """使用最后一个常用的标签以及共现标签进行初始化"""
                    if False:
                        labelWeightDF = buildWeightMatrix(fp.weightTag, fp.trainTag_csv, fp.weightTag_csv)



                    # print(labelWeightDF.shape)
                    # labelCurrenceNumpy = labelWeightDF.T.values

                    """仅使用共现标签进行初始化"""
                    # labelWeightDF = buildWeightMatrixByLabel_cooccurence(fp.weightTag,fp.trainTag_csv, fp.trainTag,fp.linkCreateTagOccurrenceNumber, hiddenCellNumber, outputCellNumber, fp.labelOccurrence_csv)
                    # labelCurrenceNumpy = labelWeightDF.T.values
                    # print("标签共现矩阵")
                    # print( labelWeightDF.shape)
                    #
                    # sizeX = y.size()[1]
                    # if int(inputCellNumber*1.2)>labelWeightDF.shape[0]:
                    #     sizeY = int(inputCellNumber*1.2)-labelWeightDF.shape[0]
                    #     print(sizeX)
                    #     print(sizeY)
                    #     zeroNumpy = np.random.rand(sizeX, sizeY)
                    #
                    #     # print(type(labelCurrenceNumpy))
                    #     # print(zeroNumpy.size())
                    #     wieghtValue = torch.FloatTensor(np.column_stack([labelCurrenceNumpy, zeroNumpy]))
                    #     print(wieghtValue.size())
                    # else:
                    #     print(u"label共现矩阵")
                    #     print(hiddenCellNumber)
                    #     print(type(labelCurrenceNumpy))
                    #     wieghtValue = torch.FloatTensor(labelCurrenceNumpy[:,:hiddenCellNumber])
                    #     print(wieghtValue.size())
                    # BPnet.predict.weight = Parameter(wieghtValue)

                    # # print(BPnet.hidden.weight)
                    # # print('---------------')
                    #     # torch.nn.Hardtanh(),
                    #     # torch.nn.Tanh(),
                    #     # torch.nn.ReLU(),
                    #     # torch.nn.Sigmoid(),
                    #
                    optimizer = torch.optim.Adam(BPnet.parameters(),lr=learning_rate)



                    # optimizer = torch.optim.SGD(BPnet.parameters(),lr=0.05)
                    loss_func = torch.nn.MultiLabelSoftMarginLoss()

                    # loss_func = torch.nn.CrossEntropyLoss()
                    try:
                        if cudaFlag:
                            BPnet.cuda()
                            loss_func.cuda()

                        print(BPnet)

                        to = time()
                        for i in range(epoch):
                            if cudaFlag:
                                out = BPnet(x.cuda())
                                loss = loss_func(out, y.cuda())  ###计算两者之间的误差
                            else:
                                out = BPnet(x)
                                # print(outputCellNumber)
                                loss = loss_func(out, y)  ###计算两者之间的误差

                            # print(out.size())



                            optimizer.zero_grad()   ###清空上一步的残余更新参数值
                            loss.backward()         ###误差反向传播，计算参数更新值
                            optimizer.step()        ###将参数更新值施加到net的参数上
                            # if i%5 == 0:
                                # print computePrecession(out,y,topK)
                            # print computePrecession(out, y, topLs)
                        #     if i%2==0:
                        #         prediction = torch.max(F.softmax(out),1)[1]
                        #         pred_y = prediction.data.numpy().squeeze()
                        #         target_y = y.data.numpy()
                        # #         plt.cla()
                        # #         plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=pred_y, s=100, lw=0, cmap='RdYlGn')
                        # #         accuracy = sum(pred_y == target_y)/200
                        # #         plt.text(1.5,-4,'accuracy=%.4f' % accuracy,fontdict={'size':20,'color':'red'})
                        # #         plt.pause(0.1)
                        # #
                        # # plt.ioff()
                        # # plt.show()
                        # print out



                        # torch.save(BPnet, '../model/BPnet.pkl')
                        test_xDF = pd.read_csv(fp.doc2bow_test)
                        test_yDF = pd.read_csv(fp.testTag_csv)
                        test_x,test_y = Variable(torch.FloatTensor(test_xDF.values)),Variable(torch.FloatTensor(test_yDF.values))
                        print(test_x.size())
                        print(test_y.size())
                        t1 = time()

                        if cudaFlag:
                            test_out = BPnet(test_x.cuda())
                            t2 = time()
                            print(test_out.size())
                            print '----------------result------------------'
                            # resDict =  computePrecession(test_out.cpu(),test_y,topLs)
                            writeRecommendTag(test_out.cpu(),test_yDF,fp.recommendFilepath,fp.timeConsuming,t1-to,t2-t1)
                            print fp.recommendFilepath
                            # print resDict

                        else:
                            test_out = BPnet(test_x)
                            t2 = time()
                            print(test_out.size())
                            print '----------------result------------------'
                            # resDict =  computePrecession(test_out,test_y,topLs)
                            writeRecommendTag(test_out, test_yDF, fp.recommendFilepath,fp.timeConsuming,t1-to,t2-t1)
                            print fp.recommendFilepath


                        # print trainTime
                        #
                        # wb = Workbook()
                        # sheet1 = wb.add_sheet("BP_result",cell_overwrite_ok=True)
                        # rd = xlrd.open_workbook(fp.compareExcelPath)
                        # sheet2 = rd.sheets()[0]
                        # lineNumber = sheet2.nrows
                        # wb1 = copy(rd)
                        # sheet2 = wb1.get_sheet(0)
                        # print lineNumber
                        # index = 0
                        # for i in [1,2,3,4,5,10]:
                        #     sheet1.write(0,index*3,"top"+str(i))
                        #     sheet1.write(1,index*3,"precesion")
                        #     sheet1.write(1,index*3+1,"recall")
                        #     sheet1.write(1,index*3+2,"F1")
                        #     sheet1.write(2,index*3,resDict[i][0])
                        #     sheet1.write(2,index*3+1,resDict[i][1])
                        #     sheet1.write(2,index*3+2,resDict[i][2])
                        #     index +=1
                        # sheet1.write(2, index * 3, str(trainTime))
                        # index = 0
                        # # sheet2.write(lineNumber, 0, 'setWeight2_3_Corpus_BPresult')
                        # sheet2.write(lineNumber, 0, '0.5_Corpus_BPresult')
                        # for i in [1,2,3,4,5,10]:
                        #     sheet2.write(lineNumber,index*3+1,resDict[i][0])
                        #     sheet2.write(lineNumber,index*3+2,resDict[i][1])
                        #     sheet2.write(lineNumber,index*3+3,resDict[i][2])
                        #     index +=1
                        # # print(fp.excelpath)
                        # print(fp.excelpath)
                        # wb.save(fp.excelpath)
                        # os.remove(fp.compareExcelPath)
                        # wb1.save(fp.compareExcelPath)
                        #
                        del BPnet,loss,loss_func,out
                        del x,y,test_x,test_y,test_out,test_xDF,test_yDF
                    except Exception,e:
                        print(e)
                        break
            except Exception as e:
                pass

