#coding=utf-8

"""计算p-value"""

from scipy import stats
from xlwt import Workbook
import xlrd
import json
import pandas as pd

originPath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'

def computePRofTestCorpusNumber():
    resDict = {}
    retLs = []
    for tmpstr in ['angular', 'bitcoin', 'elasticsearch', 'owncloud', 'pydata', 'rails', 'RIOT-OS', 'symfony',
                   'tgstation', 'ceph']:
        # for tmpstr in ['ceph']:
        splitProject = unicode(originPath + tmpstr + r'项目实验/项目集划分.txt', 'utf-8')
        print(splitProject)
        with open(splitProject, 'r') as e:  ## 从项目集划分中读出项目的划分情况
            for line in e:
                retLs = json.loads(line)
        resDict[tmpstr] = retLs.__len__()
    return resDict

"""合并三表"""
# def writeCSV(projectDict, inpath, TagMulRecExcel, basicBPExcel, Corpus_3_BPExcel, Corpus_4_BPExcel,Corpus_4_110BPExcel, outpath):
def writeCSV(projectDict, inpath,excelLs, outpath):

    with open(outpath,"w") as e:
        tmpLs = ['top1_precision','top1_recall','top1_f1','top2_precision','top2_recall','top2_f1','top3_precision','top3_recall','top3_f1','top4_precision','top4_recall','top4_f1','top5_precision','top5_recall','top5_f1','top10_precision','top10_recall','top10_f1','method']
        e.write(",".join(tmpLs)+'\n')

        for projectName in projectDict:
            # if projectName != 'bitcoin':
            #     continue

            projectFile = projectName + '项目实验/'
            for excel in excelLs:
                excel_rb = xlrd.open_workbook(unicode(inpath + projectFile  +'all'+projectName+excel, 'utf-8'))
                excel_sheet = excel_rb.sheets()[0]
                tmpLs = []
                for index in xrange(excel_sheet.ncols):
                    tmpLs.append(str(excel_sheet.cell(2, index).value))
                tmpLs.append(excel.split(".")[0])
                e.write(",".join(tmpLs) + '\n')

            # TagMulRec_rb = xlrd.open_workbook(unicode(inpath + projectFile  +'all'+projectName+TagMulRecExcel, 'utf-8'))
            # BasicBP_rb = xlrd.open_workbook(unicode(inpath + projectFile  + 'all'+projectName+basicBPExcel, 'utf-8'))
            # Corpus_3_BP_rb = xlrd.open_workbook(unicode(inpath + projectFile + 'all' + projectName + Corpus_3_BPExcel, 'utf-8'))
            # Corpus_4_BP_rb = xlrd.open_workbook(unicode(inpath + projectFile + 'all' + projectName + Corpus_4_BPExcel, 'utf-8'))
            # Corpus_4_110BP_rb = xlrd.open_workbook(unicode(inpath + projectFile + 'all' + projectName + Corpus_4_110BPExcel, 'utf-8'))
            #
            # TagMulRec_sheet = TagMulRec_rb.sheets()[0]
            # BasicBP_sheet = BasicBP_rb.sheets()[0]
            # Corpus_3_BP_sheet = Corpus_3_BP_rb.sheets()[0]
            # Corpus_4_BP_sheet = Corpus_4_BP_rb.sheets()[0]
            # Corpus_4_110BP_sheet = Corpus_4_110BP_rb.sheets()[0]
            #
            # for sheet,method in [(TagMulRec_sheet,TagMulRecExcel), (BasicBP_sheet,basicBPExcel), (Corpus_3_BP_sheet, Corpus_3_BPExcel), (Corpus_4_BP_sheet, Corpus_4_BPExcel),(Corpus_4_110BP_sheet,Corpus_4_110BPExcel)]:
            #     tmpLs = []
            #     cols = sheet.ncols
            #
            #     for index in xrange(cols):
            #         tmpLs.append(str(sheet.cell(2, index).value))
            #
            #     #     if index%3 != 0:
            #     #         tmpLs.append(str(sheet.cell(2, index).value))
            #     #     else:
            #     #         if index == 0:
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     #         if index/3==1:
            #     #             tmpLs.append("top1")
            #     #             e.write(",".join(tmpLs)+'\n')
            #     #             tmpLs = []
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     #         elif index/3==2:
            #     #             tmpLs.append("top2")
            #     #             e.write(",".join(tmpLs) + '\n')
            #     #             tmpLs = []
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     #         elif index/3==3:
            #     #             tmpLs.append("top5")
            #     #             e.write(",".join(tmpLs) + '\n')
            #     #             tmpLs = []
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     #         elif index/3==4:
            #     #             tmpLs.append("top4")
            #     #             e.write(",".join(tmpLs) + '\n')
            #     #             tmpLs = []
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     #         elif index/3==5:
            #     #             tmpLs.append("top5")
            #     #             e.write(",".join(tmpLs) + '\n')
            #     #             tmpLs = []
            #     #             tmpLs.append(str(sheet.cell(2, index).value))
            #     # tmpLs.append("top10")
            #     tmpLs.append(method.split(".")[0])
            #     e.write(",".join(tmpLs) + '\n')
            #
            # print(cols)



# basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
# projectDict = computePRofTestCorpusNumber()
#
#
# """合并三表"""
# TagMulRec = 'tagMulRecRes.xls'
# corpus_1_BP = '1_Corpus_BPresult.xls'
# corpus_3_BP = '3_Corpus_BPresult.xls'
# # # # BasicBP = '0.9_BPresult.xls'
# # # # SetWeight = 'setWeight_BPresult.xls'
# corpus_4_BP = '4_Corpus_BPresult.xls'
# corpus_4_110BP = '110_Corpus_BPresult.xls'
outpath = '/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/三种情形的实验对比结果1.csv'
df = pd.read_csv(outpath,sep=",")
# # #
# excelLs = [ TagMulRec, corpus_1_BP, corpus_3_BP, corpus_4_BP, corpus_4_110BP]
# writeCSV(projectDict, basicFilepath,excelLs,outpath)

projectDict = {'symfony': 6, 'tgstation': 6, 'pydata': 4, 'bitcoin': 1, 'rails': 6, 'ceph': 7, 'owncloud': 8,
                   'elasticsearch': 8, 'angular': 9, 'RIOT-OS': 6}
basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'

for projectName in projectDict:

    # if projectName not in ['angular']:
    #     continue

    projectFile = projectName + '项目实验/'
    for i in xrange(1, projectDict[projectName] + 1):
        trainNumberFile = '第' + str(i) + '次训练/'
        TagMulRec_Csv = unicode(basicFilepath + projectFile + trainNumberFile + '推荐结果/' + 'TagMulRecRes_PerPR.csv', 'utf-8')
        BPRec_Csv = unicode(basicFilepath + projectFile + trainNumberFile + '推荐结果/' + '1_40_0.005_2000_Corpus_BPresult_PerPR.csv', 'utf-8')
        if i == 1:
            TagMulRec_DF = pd.read_csv(TagMulRec_Csv,sep=",")
            BPRec_DF = pd.read_csv(BPRec_Csv,sep=",")
        else:
            TagMulRec_DF = pd.concat([TagMulRec_DF,pd.read_csv(TagMulRec_Csv, sep=",")],axis=0)
            BPRec_DF = pd.concat([BPRec_DF,pd.read_csv(BPRec_Csv, sep=",")],axis=0)

    # projectFile = projectName + '项目实验/'
    # TagMulRec_outpath = unicode(basicFilepath + projectFile + '/pValue计算结果/TagMulRes.csv', 'utf-8')
    # BPRes_outpath = unicode(basicFilepath + projectFile + '/pValue计算结果/BPRes.csv', 'utf-8')
    #
    # BP_df = pd.read_csv(BPRes_outpath,sep=",")
    # TagMulRec_df = pd.read_csv(TagMulRec_outpath,sep=",")
    tmpLs = ['top1_precision', 'top1_recall', 'top1_f1', 'top2_precision', 'top2_recall', 'top2_f1', 'top3_precision',
             'top3_recall', 'top3_f1', 'top4_precision', 'top4_recall', 'top4_f1', 'top5_precision', 'top5_recall',
             'top5_f1', 'top10_precision', 'top10_recall', 'top10_f1']

        # pValueDict ={
        #     'tagMulRec_4CorpusBP':['tagMulRecRes','4_Corpus_BPresult'],
        #     '4CorpusBP_110CorpusBP':['4_Corpus_BPresult','110_Corpus_BPresult'],
        #              }
        # for key in pValueDict:
        # with open(basicFilepath + projectFile + '/pValue计算结果/_p-value.txt','w') as e:
    # pValueDict ={
    #     'tagMulRec_4CorpusBP':['tagMulRecRes','4_Corpus_BPresult'],
    #     '4CorpusBP_110CorpusBP':['4_Corpus_BPresult','110_Corpus_BPresult'],
    #              }
    # for key in pValueDict:
    with open('/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'+projectName+'项目实验/pValue计算结果/t_pValue.txt','w') as e:
        for val in tmpLs:
            df1 = TagMulRec_DF[val]
            df2 = BPRec_DF[val]

            args = [df2,df1]
            resLs = []
            resLs.append(val)
            resLs.append(stats.f_oneway(*args))
            e.write(json.dumps(resLs)+'\n')
            # print(resLs)

