#coding=utf-8

import xlrd
import xlwt
from smallcorpusTrain import smallCorpusTrain
from xlwt import Workbook
from xlutils.copy import copy
import json

"""flag = 0或者1 根据excel表中第一列的值决定"""
def computeAverage(inpath,projectDict,excelName,flag=1):
    for projectName in projectDict:

        projectFile = projectName + '项目实验/'

        wb = Workbook()
        resSheet = wb.add_sheet('BPResult', cell_overwrite_ok=True)

        colIndex=0
        for tmpi in [1, 2, 3, 4, 5, 10]:
            resSheet.write(0, colIndex, 'top' + str(tmpi))
            resSheet.write(1, colIndex, 'precision')
            resSheet.write(1, colIndex + 1, 'recall')
            resSheet.write(1, colIndex + 2, 'f1')
            colIndex+=3


        BPprecisionDict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}  ##存储excel中每次训练的结果,这里top10以下标6的形式记录
        BPrecallDict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}  ##存储excel中每次训练的结果
        BPF1Dict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}  ##存储excel中每次训练的结果

        for i in xrange(1, projectDict[projectName] + 1):

            trainNumberFile = '第' + str(i) + '次训练/'

            try:
                rb = xlrd.open_workbook(unicode(inpath + projectFile + trainNumberFile+'推荐结果/' +excelName, 'utf-8'))
            except IOError as e:
                print(unicode(inpath + projectFile + trainNumberFile +'推荐结果/'+excelName, 'utf-8'))

            sheet1 = rb.sheets()[0]

            if flag:

                if excelName == '100_Corpus_BPresult.xls':
                    cols = sheet1.ncols
                else:
                    cols = sheet1.ncols - 1

                for j in range(0, cols):
                    if j % 3 == 0:
                        BPprecisionDict[j / 3 + 1].append(sheet1.cell(2, j).value)
                    elif (j - 1) % 3 == 0:
                        BPrecallDict[(j - 1) / 3 + 1].append(sheet1.cell(2, j).value)
                    elif (j - 2) % 3 == 0:
                        BPF1Dict[(j - 2) / 3 + 1].append(sheet1.cell(2, j).value)
            else:
                cols = sheet1.ncols
                for j in range(1, cols):
                    if (j-1) % 3 == 0:
                        BPprecisionDict[(j-1) / 3 + 1].append(sheet1.cell(2, j).value)
                    elif (j - 2) % 3 == 0:
                        BPrecallDict[(j - 2) / 3 + 1].append(sheet1.cell(2, j).value)
                    elif (j - 3) % 3 == 0:
                        BPF1Dict[(j - 3) / 3 + 1].append(sheet1.cell(2, j).value)
        colIndex = 0
        for i in [1, 2, 3, 4, 5, 6]:
            BPprecisionValue = sum(BPprecisionDict[i]) / len(BPprecisionDict[i])
            BPrecallValue = sum(BPrecallDict[i]) / len(BPrecallDict[i])
            try:
                BPF1Value = sum(BPF1Dict[i]) / len(BPF1Dict[i])
            except ZeroDivisionError,e:
                print(inpath + projectFile + trainNumberFile +excelName)

            resSheet.write(2, colIndex, BPprecisionValue)
            resSheet.write(2, colIndex + 1, BPrecallValue)
            resSheet.write(2, colIndex + 2, BPF1Value)
            colIndex += 3
        wb.save(unicode(inpath + projectFile  + 'average'+projectName+excelName, 'utf-8'))

"""计算项目的训练时间"""
def computeAverageTime(inpath,projectDict,excelName,trainFlag=1):
    for projectName in projectDict:
        # if projectName not in ['angular']:
        #     continue

        projectFile = projectName + '项目实验/'

        wb = Workbook()
        resSheet = wb.add_sheet('FNNRec_TimeConsuming', cell_overwrite_ok=True)


        trainingTimeSum = 0
        predictTimeSum = 0
        for i in xrange(1, projectDict[projectName] + 1):

            trainNumberFile = '第' + str(i) + '次训练/'
            with open(unicode(inpath + projectFile + trainNumberFile+'推荐结果/' +excelName, 'utf-8'),'r') as e:
                for line in e:
                    data = json.loads(line)
                    trainingTimeSum += data[0]
                    if trainFlag:
                        predictTimeSum += data[1]
        resSheet.write(0,0,'Project')
        resSheet.write(0,1,'trainingTime')
        resSheet.write(1,0,projectName)
        resSheet.write(1,1,trainingTimeSum/projectDict[projectName])
        if trainFlag:
            resSheet.write(0,2,'predictTime')
            resSheet.write(1,2,predictTimeSum/projectDict[projectName])
        tmpexcelName = excelName[:-4]
        wb.save(unicode(inpath + projectFile  + 'average'+projectName+tmpexcelName+'.xls', 'utf-8'))

def mergeAllRes(inpath,projectDict,excelName,flag=1):
    for projectName in projectDict:

        # if projectName not in ['ceph']:
        #     continue

        projectFile = projectName + '项目实验/'
        if flag:

            outpath = unicode(inpath + projectFile  + '/pValue计算结果/TagMulRes.csv', 'utf-8')
        else:
            outpath = unicode(inpath + projectFile  + '/pValue计算结果/BPRes.csv', 'utf-8')
        print(outpath)
        resLs = []
        with open(outpath,"w") as e:

            for tmpi in [1, 2, 3, 4, 5, 10]:
                resLs.append('top' + str(tmpi)+'_precision')
                resLs.append('top' + str(tmpi)+'_recall')
                resLs.append('top' + str(tmpi)+'_f1')
            e.write(",".join(resLs)+'\n')
            resLs = []

            for i in xrange(1, projectDict[projectName] + 1):
                trainNumberFile = '第' + str(i) + '次训练/'
                try:
                    rb = xlrd.open_workbook(unicode(inpath + projectFile + trainNumberFile+'推荐结果/' +excelName, 'utf-8'))
                except IOError as e1:
                    print(unicode(inpath + projectFile + trainNumberFile +'推荐结果/'+excelName, 'utf-8'))

                sheet1 = rb.sheets()[0]

                cols = sheet1.ncols
                if flag:
                    for j in range(0, cols):
                        resLs.append(str(sheet1.cell(2, j).value))
                else:
                    for j in range(1, cols):
                        resLs.append(str(sheet1.cell(2, j).value))
                e.write(",".join(resLs) + '\n')
                resLs = []

"""合并三表"""
def mergeThreeExcel(projectDict,inpath,TagMulRecExcel,basicBPExcel,SetweightExcel,lastmonth,outpath):
    wb = Workbook()
    resSheet = wb.add_sheet('BPResult', cell_overwrite_ok=True)
    index = 0
    for tmpi in [1, 2, 3, 4, 5, 10]:
        resSheet.write(0, index + 2, 'top' + str(tmpi))
        resSheet.write(1, index + 2, 'precision')
        resSheet.write(1, index + 3, 'recall')
        resSheet.write(1, index + 4, 'f1')
        index += 3
    rowNumber = 2
    for projectName in projectDict:
        # if projectName != 'symfony':
        #     continue

        projectFile = projectName + '项目实验/'
        TagMulRec_rb = xlrd.open_workbook(unicode(inpath + projectFile  +'all'+projectName+TagMulRecExcel, 'utf-8'))
        BasicBP_rb = xlrd.open_workbook(unicode(inpath + projectFile  + 'all'+projectName+basicBPExcel, 'utf-8'))
        setWeght_rb = xlrd.open_workbook(unicode(inpath + projectFile  + 'all'+projectName+SetweightExcel, 'utf-8'))
        lastmonth_rb = xlrd.open_workbook(unicode(inpath + projectFile  + 'all'+projectName+lastmonth, 'utf-8'))

        TagMulRec_sheet = TagMulRec_rb.sheets()[0]
        BasicBP_sheet = BasicBP_rb.sheets()[0]
        setWeght_sheet = setWeght_rb.sheets()[0]
        lastmonth_sheet = lastmonth_rb.sheets()[0]

        cols = TagMulRec_sheet.ncols

        resSheet.write(rowNumber,0,projectName)
        resSheet.write(rowNumber,1,TagMulRecExcel)
        resSheet.write(rowNumber+12,1,basicBPExcel)
        resSheet.write(rowNumber+24,1,SetweightExcel)
        resSheet.write(rowNumber+36,1,lastmonth)

        for j in range(0, cols):
            resSheet.write(rowNumber,j+2,TagMulRec_sheet.cell(2,j).value)
            resSheet.write(rowNumber+12,j+2,BasicBP_sheet.cell(2,j).value)
            resSheet.write(rowNumber+24,j+2,setWeght_sheet.cell(2,j).value)
            resSheet.write(rowNumber+36,j+2,lastmonth_sheet.cell(2,j).value)
        rowNumber+=1


    wb.save(outpath)

"""合并参数得到的表"""
def mergeParameterExcel(projectDict,inpath,TagMulRecExcel,outpath):
    wb = Workbook()
    resSheet = wb.add_sheet('BPResult', cell_overwrite_ok=True)
    index = 0
    for tmpi in [1, 2, 3, 4, 5, 10]:
        resSheet.write(0, index + 2, 'top' + str(tmpi))
        resSheet.write(1, index + 2, 'precision')
        resSheet.write(1, index + 3, 'recall')
        resSheet.write(1, index + 4, 'f1')
        index += 3
    rowNumber = 2
    for projectName in projectDict:
        # if projectName != 'symfony':
        #     continue

        projectFile = projectName + '项目实验/'
        TagMulRec_rb = xlrd.open_workbook(unicode(inpath + projectFile  +'average'+projectName+TagMulRecExcel, 'utf-8'))


        TagMulRec_sheet = TagMulRec_rb.sheets()[0]

        cols = TagMulRec_sheet.ncols

        resSheet.write(rowNumber,0,projectName)
        resSheet.write(rowNumber,1,TagMulRecExcel)


        for j in range(0, cols):
            resSheet.write(rowNumber,j+2,TagMulRec_sheet.cell(2,j).value)

        rowNumber+=1


    wb.save(outpath)

"""合并参数得到的表"""
def mergeTimeConsumingExcel(projectDict, inpath, TimeConsuming, outpath,trainFlag=1):
    wb = Workbook()
    resSheet = wb.add_sheet('FNNRec_TimeConsuming', cell_overwrite_ok=True)
    resSheet.write(0, 0, 'project')
    resSheet.write(0, 1, 'trainingTime')
    resSheet.write(0, 2, 'predictTime')
    rowNumber = 1
    for projectName in projectDict:
        # if projectName not in ['angular']:
        #     continue
        projectFile = projectName + '项目实验/'
        TagMulRec_rb = xlrd.open_workbook(unicode(inpath + projectFile +'average' + projectName + TimeConsuming, 'utf-8'))
        TagMulRec_sheet = TagMulRec_rb.sheets()[0]

        resSheet.write(rowNumber,0,TagMulRec_sheet.cell(1,0).value)
        resSheet.write(rowNumber,1,TagMulRec_sheet.cell(1,1).value)
        if trainFlag:
            resSheet.write(rowNumber,2,TagMulRec_sheet.cell(1,2).value)
        rowNumber+=1

    wb.save(outpath)


def mergeTagMulResAndBPRes():
    outpath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/三个项目的实验对比结果2.xls'

    allProjectWb = Workbook()
    allProjectSheet = allProjectWb.add_sheet('allProjectResult', cell_overwrite_ok=True)
    index = 0
    for tmpi in [1, 2, 3, 4, 5, 10]:
        allProjectSheet.write(0, index+2, 'top' + str(tmpi))
        allProjectSheet.write(1, index+2, 'precision')
        allProjectSheet.write(1, index + 3, 'recall')
        allProjectSheet.write(1, index + 4, 'f1')
        index += 3
    allProjectSheet_line = 2

    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验/'
    projectDict = smallCorpusTrain.computePRofTestCorpusNumber()
    print(projectDict)
    for projectName in projectDict:
        BPprecisionDict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果,这里top10以下标6的形式记录
        BPrecallDict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果
        BPF1Dict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果

        TagMulprecisionDict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果
        TagMulrecallDict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果
        TagMulF1Dict = {1:[],2:[],3:[],4:[],5:[],6:[]} ##存储excel中每次训练的结果

        # if projectName not in ['ceph','symfony','owncloud']:
        if projectName != 'tgstation':
            continue
        projectFile = projectName + '项目实验/'

        wb = Workbook()
        wb1 = Workbook()
        allBPRes_sheet = wb.add_sheet('result', cell_overwrite_ok=True)
        allTagMulRecRes_sheet = wb1.add_sheet('result', cell_overwrite_ok=True)
        lineNumber = 2
        lineNumber1 = 2

        index = 0
        for tmpi in [1, 2, 3, 4, 5, 10]:
            allBPRes_sheet.write(0, index, 'top' + str(tmpi))
            allBPRes_sheet.write(1, index, 'precision')
            allBPRes_sheet.write(1, index + 1, 'recall')
            allBPRes_sheet.write(1, index + 2, 'f1')

            allTagMulRecRes_sheet.write(0, index, 'top' + str(tmpi))
            allTagMulRecRes_sheet.write(1, index, 'precision')
            allTagMulRecRes_sheet.write(1, index + 1, 'recall')
            allTagMulRecRes_sheet.write(1, index + 2, 'f1')

            index += 3

        for i in xrange(1, projectDict[projectName] + 1):
        # for i in xrange(1, 2):

            trainNumberFile = '第' + str(i) + '次训练/'
            trainBasicFile = basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
            testBasicFile = basicFilepath + projectFile + trainNumberFile + 'testCorpus/'

            resultExcel = unicode(basicFilepath + projectFile + trainNumberFile + 'tagMulRecRes.xls','utf-8')
            TagMulRec_rd = xlrd.open_workbook(resultExcel)
            TagMulRec_sheet = TagMulRec_rd.sheets()[0]
            TagMulRec_ncols = TagMulRec_sheet.ncols
            print(TagMulRec_ncols)

            try:
                for j in range(1,TagMulRec_ncols):
                    if projectName == 'ceph':  ##由于ceph项目计算了好几次的对比结果，所以需要采用特殊处理
                        if (j-1)%3 == 0:
                            TagMulprecisionDict[(j-1)/3+1].append(TagMulRec_sheet.cell(2, j).value)
                            BPprecisionDict[(j-1)/3+1].append(TagMulRec_sheet.cell(4, j).value)
                        elif (j-2)%3 == 0:
                            TagMulrecallDict[(j -2) / 3 + 1].append(TagMulRec_sheet.cell(2, j).value)
                            BPrecallDict[(j -2) / 3 + 1].append(TagMulRec_sheet.cell(4, j).value)
                        elif (j-3)%3 == 0:
                            TagMulF1Dict[(j -3) / 3 + 1].append(TagMulRec_sheet.cell(2, j).value)
                            BPF1Dict[(j -3) / 3 + 1].append(TagMulRec_sheet.cell(4, j).value)
                    else:
                        if (j-1)%3 == 0:
                            TagMulprecisionDict[(j-1)/3+1].append(TagMulRec_sheet.cell(2, j).value)
                            BPprecisionDict[(j-1)/3+1].append(TagMulRec_sheet.cell(3, j).value)
                        elif (j-2)%3 == 0:
                            TagMulrecallDict[(j -2) / 3 + 1].append(TagMulRec_sheet.cell(2, j).value)
                            BPrecallDict[(j -2) / 3 + 1].append(TagMulRec_sheet.cell(3, j).value)
                        elif (j-3)%3 == 0:
                            TagMulF1Dict[(j -3) / 3 + 1].append(TagMulRec_sheet.cell(2, j).value)
                            BPF1Dict[(j -3) / 3 + 1].append(TagMulRec_sheet.cell(3, j).value)
            except IndexError as e:
                print("===="+projectName)
                print("===="+j)
        colIndex = 0
        allProjectSheet.write(allProjectSheet_line, colIndex, projectName)
        allProjectSheet.write(allProjectSheet_line, colIndex+1, "TagMulRec")
        allProjectSheet.write(allProjectSheet_line+1, colIndex+1, "BP")
        for i in [1,2,3,4,5,6]:
            BPprecisionValue = sum(BPprecisionDict[i]) / len(BPprecisionDict[i])
            BPrecallValue = sum(BPrecallDict[i]) / len(BPrecallDict[i])
            BPF1Value = sum(BPF1Dict[i]) / len(BPF1Dict[i])

            TagMulprecisionValue = sum(TagMulprecisionDict[i]) / len(TagMulprecisionDict[i])
            TagMulrecallValue = sum(TagMulrecallDict[i]) / len(TagMulrecallDict[i])
            TagMulF1Value = sum(TagMulF1Dict[i]) / len(TagMulF1Dict[i])

            allTagMulRecRes_sheet.write(lineNumber, colIndex, TagMulprecisionValue)
            allTagMulRecRes_sheet.write(lineNumber, colIndex + 1, TagMulrecallValue)
            allTagMulRecRes_sheet.write(lineNumber, colIndex + 2, TagMulF1Value)
            allBPRes_sheet.write(lineNumber1,colIndex,BPprecisionValue)
            allBPRes_sheet.write(lineNumber1,colIndex+1,BPrecallValue)
            allBPRes_sheet.write(lineNumber1,colIndex+2,BPF1Value)


            allProjectSheet.write(allProjectSheet_line,colIndex+2,TagMulprecisionValue)
            allProjectSheet.write(allProjectSheet_line,colIndex+3,TagMulrecallValue)
            allProjectSheet.write(allProjectSheet_line,colIndex+4,TagMulF1Value)
            allProjectSheet.write(allProjectSheet_line+1,colIndex+2,BPprecisionValue)
            allProjectSheet.write(allProjectSheet_line+1,colIndex+3,BPrecallValue)
            allProjectSheet.write(allProjectSheet_line+1,colIndex+4,BPF1Value)

            colIndex+=3

        lineNumber+=1
        lineNumber1+=1
        allProjectSheet_line+=4

        wb.save(unicode(basicFilepath + projectFile +projectName+ '_allBRresult.xls','utf-8'))
        wb1.save(unicode(basicFilepath + projectFile + projectName+'_allTagMulRecRes.xls','utf-8'))

        allProjectWb.save(unicode(outpath,'utf-8'))

def computePRofTestCorpusNumber(originPath,parameter=3000):
    resDict = {}
    retLs = []

    for tmpstr in ['angular','bitcoin','elasticsearch','owncloud','pydata','rails','RIOT-OS','symfony','tgstation','ceph']:
        # if parameter == 3000:
        #     splitProject = unicode(originPath + tmpstr + r'项目实验/项目集划分.txt', 'utf-8')
        # else:
        splitProject = unicode(originPath+ tmpstr + r'项目实验/'+str(parameter)+'项目集划分.txt','utf-8')
        print(splitProject)
        with open(splitProject, 'r') as e:  ## 从项目集划分中读出项目的划分情况
            for line in e:
                retLs = json.loads(line)
        resDict[tmpstr] = retLs.__len__()
    return resDict

def copyFile(projectDict,hiddenNeurons,epoch,learning_rate,parameter):
    inPath = r'/media/mamile/A2F2CB0DF2CAE51F/10个项目的BP神经网络实验(过滤训练集标签)/'
    outPath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    for projectName in projectDict:
        # if projectName != 'angular':
        #     continue
        for index in xrange(1,projectDict[projectName]+1):
            projectFile = projectName + '项目实验/'
            trainNumberFile = '第' + str(index) + '次训练/'
            testBasicFile_In = inPath + projectFile + trainNumberFile + 'testCorpus/'
            testBasicFile_Out = outPath + projectFile + trainNumberFile + 'testCorpus/'

            timeConsume_In = inPath + projectFile + trainNumberFile + '推荐结果/'+ str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(
                                parameter) + 'timeCosuming.txt'
            timeConsume_Out = outPath + projectFile + trainNumberFile + '推荐结果/'+ str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(
                                parameter) + 'timeCosuming.txt'
            recommendFilepath_In = unicode(
            testBasicFile_In + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(
                    parameter) + '_BP_filepath_recommend_tag.txt', 'utf-8')
            recommendFilepath_Out = unicode(
                testBasicFile_Out + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(
                                parameter) + '_BP_filepath_recommend_tag.txt', 'utf-8')
            with open(recommendFilepath_Out,"w") as e:
                with open(recommendFilepath_In,"r") as e1:
                    for line in e1:
                        e.write(line)
            # with open(timeConsume_Out,"w") as e:
            #     with open(timeConsume_In,"r") as e1:
            #         for line in e1:
            #             e.write(line)

if __name__ == '__main__':

    """文件拷贝"""
    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    #basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(2个月)/'
    epoch, learning_rate = 40,0.005
    parameter = 2000
    projectDict = computePRofTestCorpusNumber(basicFilepath,parameter)
    print(projectDict)
    # for hiddenNeurons in [1]:
    #     copyFile(projectDict,hiddenNeurons,epoch,learning_rate,parameter)



    """计算各个项目各种实验的平均值"""
    excelNameLs = ['1_40_0.005_2000_BP_allcorpus_recommend_tag.xls']
    for excelName in excelNameLs:
        computeAverage(basicFilepath,projectDict,excelName,flag=0)

    for excelName in excelNameLs:
        outpath = '/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/2_average_all'+excelName
        # outpath = '/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(5个月)/average_all'+excelName
        mergeParameterExcel(projectDict, basicFilepath, excelName,outpath)

    """计算各个项目的平均训练时间和测试时间"""
    # timeFile = '1_200_0.005_2000timeCosuming.txt'
    # excelName = '1_200_0.005_2000timeCosuming.xls'
    # outpath = '/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/average_all' + excelName
    # computeAverageTime(basicFilepath,projectDict,timeFile,trainFlag=1)
    # mergeTimeConsumingExcel(projectDict, basicFilepath, excelName, outpath,trainFlag=1)