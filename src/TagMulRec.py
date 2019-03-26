#coding=utf-8

from gensim import corpora,models
from nltkGenerateWord import Corpus,Tags
import math
import json
from xlwt import Workbook
from projectSelect.smallcorpusTrain import smallCorpusTrain
from time import time

class TagMulRec:

    """对比方法"""

    """计算两个对象之间的(Fai)o和oi"""
    @staticmethod
    def computeFirstPart(sentenceO,sentenceOi):
        commonWordNumber = [word for word in sentenceO if word in sentenceOi].__len__()
        if sentenceOi.__len__() == 0:
            return 0
        else:
            return float(commonWordNumber)/sentenceOi.__len__()

    """计算word在sentence中的频率"""
    @staticmethod
    def computeWordFrequenceInSentence(sentence,word):
        if sentence.__len__() == 0:
            return 0
        else:
            wordNumber = sum([1 for val in sentence if val ==word])
            return float(wordNumber)/sentence.__len__()


    """得到语料库中包含word的sentnce个数字典"""
    @staticmethod
    def computeWSentenceDictInCorpus(corpus_sentence,wordLs):
        resDict = {}
        for word in wordLs:
            resDict[word]=0
            for sentence in corpus_sentence:
                if word in sentence:
                    resDict[word]+=1
        return resDict

    """计算第二部分得分"""
    @staticmethod
    def computeSecondPart(sentenceO,wordSentenceNumberDict,sentenceOweight=1,wordWeightDict={}):
        result = 0
        for word in sentenceO:
            if word not in wordSentenceNumberDict:
                result+=0
            else:
                result+= 1.0/math.sqrt(sentenceOweight*sentenceOweight*wordSentenceNumberDict[word])
        return result

    """计算第三部分"""
    @staticmethod
    def computeThirdPart(sentenceO,sentenceOi,sentenceOiweight=1):
        result = 0
        for word in sentenceO:

            if len(sentenceOi) == 0:
                result+=0
            else:
                OiwFrequency = TagMulRec.computeWordFrequenceInSentence(sentenceOi, word)
                pOid = sentenceOiweight/float(math.sqrt(len(sentenceOi)))
                result +=OiwFrequency*pOid
        return result


    """计算O和Oi之间的分数"""
    @staticmethod
    def computeScore(sentenceO,sentenceLs,wordSentenceNumberDict):
        resDict = {}
        i = 0
        for sentenceOi in sentenceLs:
            i += 1
            firstPart = TagMulRec.computeFirstPart(sentenceO,sentenceOi)
            secondPart = TagMulRec.computeSecondPart(sentenceO,wordSentenceNumberDict)
            thirdPart = TagMulRec.computeThirdPart(sentenceO,sentenceOi)
            resDict[i] = firstPart*secondPart*thirdPart
        return resDict

    """推荐标签"""
    @staticmethod
    def recommendTag(trainTagFile,scoreDict):
        tagSet = set()
        tagTextDict = {}
        tagScoreDict = {}
        lineNumber = 0
        with open(trainTagFile,'r') as e:
            for line in e:
                lineNumber+=1
                data = json.loads(line)
                for tag in data:
                    tagSet.add(tag)
                tagTextDict[lineNumber] = data
        maxValue,minValue = max(scoreDict.values()),min(scoreDict.values())
        if maxValue != minValue:
            for key in scoreDict:
                scoreDict[key] = (scoreDict[key] - minValue) / (maxValue - minValue)

        for tag in tagSet:
            tmp = 0
            for key in scoreDict:
                if tag in tagTextDict[key]:
                   tmp += scoreDict[key]
            tagScoreDict[tag] = tmp
        return sorted(tagScoreDict.items(),key=lambda x:x[1],reverse=True)

    @staticmethod
    def computePercision_Recall(recommendTagFile,actualTagFile,topKLs):
        precesionDict ={}
        recallDict ={}
        F1Dict ={}


        recommendTagDict = Tags.getDict(recommendTagFile)
        actualTagTagDict = Tags.getDict1(actualTagFile)

        for K in topKLs:
            precesionLs = []
            recallLs = []
            F1Ls = []
            for i in xrange(recommendTagDict.__len__()):
                rightNumber = list(set(recommendTagDict[i][:K]) & set(actualTagTagDict[i])).__len__()
                precision = float(rightNumber)/K
                recall = float(rightNumber)/actualTagTagDict[i].__len__()
                if precision+recall == 0:
                    F1 = 0.0
                else:
                    F1 = 2*precision*recall/(precision+recall)
                precesionLs.append(precision)
                recallLs.append(recall)
                F1Ls.append(F1)
            precesionDict[K] = sum(precesionLs)/precesionLs.__len__()
            recallDict[K] = sum(recallLs)/recallLs.__len__()
            F1Dict[K] = sum(F1Ls)/F1Ls.__len__()
        return precesionDict,recallDict,F1Dict

    @staticmethod
    def computePercision_Recall_PerPR(recommendTagFile, actualTagFile, topKLs,outpath):

        recommendTagDict = Tags.getDict(recommendTagFile)
        actualTagTagDict = Tags.getDict1(actualTagFile)

        with open(outpath,"w") as e:
            e.write(",".join(['top1_precision', 'top1_recall', 'top1_f1', 'top2_precision', 'top2_recall', 'top2_f1', 'top3_precision',
             'top3_recall', 'top3_f1', 'top4_precision', 'top4_recall', 'top4_f1', 'top5_precision', 'top5_recall',
             'top5_f1', 'top10_precision', 'top10_recall', 'top10_f1'])+'\n')
            for i in xrange(recommendTagDict.__len__()):
                resLs = []
                for K in topKLs:
                    rightNumber = list(set(recommendTagDict[i][:K]) & set(actualTagTagDict[i])).__len__()
                    precesion= float(rightNumber) / K
                    recall = float(rightNumber) / actualTagTagDict[i].__len__()
                    if precesion + recall == 0:
                        F1 = 0.0
                    else:
                        F1 = 2 * precesion * recall / (precesion + recall)
                    resLs.extend([str(precesion),str(recall),str(F1)])
                e.write(",".join(resLs)+'\n')

    @staticmethod
    def BP_computePercision_Recall(recommendTagFile, actualTagFile, topKLs):
        precesionDict = {}
        recallDict = {}
        F1Dict = {}

        recommendTagDict = Tags.getDict1(recommendTagFile)
        print(actualTagFile)
        actualTagTagDict = Tags.getDict1(actualTagFile)

        for K in topKLs:
            precesionLs = []
            recallLs = []
            F1Ls = []
            for i in xrange(recommendTagDict.__len__()):
                if(actualTagTagDict.__len__()<i+1):
                    break
                rightNumber = list(set(recommendTagDict[i][:K]) & set(actualTagTagDict[i])).__len__()
                precision = float(rightNumber) / K
                recall = float(rightNumber) / actualTagTagDict[i].__len__()
                if precision + recall == 0:
                    F1 = 0.0
                else:
                    F1 = 2 * precision * recall / (precision + recall)
                precesionLs.append(precision)
                recallLs.append(recall)
                F1Ls.append(F1)
            precesionDict[K] = sum(precesionLs) / precesionLs.__len__()
            recallDict[K] = sum(recallLs) / recallLs.__len__()
            F1Dict[K] = sum(F1Ls) / F1Ls.__len__()
        return precesionDict, recallDict, F1Dict

    """计算每个pull request的准确率,召回率和F1并写入文件"""
    @staticmethod
    def BP_computePercision_Recall_PerPR(recommendTagFile, actualTagFile, topKLs,outpath):

        recommendTagDict = Tags.getDict1(recommendTagFile)
        actualTagTagDict = Tags.getDict1(actualTagFile)

        with open(outpath,"w") as e:
            e.write(",".join(['top1_precision', 'top1_recall', 'top1_f1', 'top2_precision', 'top2_recall', 'top2_f1',
                              'top3_precision',
                              'top3_recall', 'top3_f1', 'top4_precision', 'top4_recall', 'top4_f1', 'top5_precision',
                              'top5_recall',
                              'top5_f1', 'top10_precision', 'top10_recall', 'top10_f1']) + '\n')
            for i in xrange(recommendTagDict.__len__()):
                resLs = []
                for K in topKLs:
                    rightNumber = list(set(recommendTagDict[i][:K]) & set(actualTagTagDict[i])).__len__()
                    precision = float(rightNumber) / K
                    recall = float(rightNumber) / actualTagTagDict[i].__len__()

                    if precision + recall == 0:
                        F1 = 0.0
                    else:
                        F1 = 2 * precision * recall / (precision + recall)
                    resLs.append(str(precision))
                    resLs.append(str(recall))
                    resLs.append(str(F1))
                e.write(",".join(resLs)+'\n')

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

if __name__ == '__main__':

    hiddenNeurons = 1
    epoch = 40
    learning_rate = 0.005
    parameter = 2000

    """第一步: 推荐标签"""
    basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
    #basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(2个月)/'
    projectDict = computePRofTestCorpusNumber(basicFilepath,parameter)
    print(projectDict)
    topKLs = [1, 2, 3, 4, 5, 10]
    for projectName in projectDict:
        if projectName == 'bitcoin' and parameter == 4000:
            continue
        projectFile = projectName + '项目实验/'
        for i in xrange(1, projectDict[projectName] + 1):
        # for i in xrange(1, 2):

            trainNumberFile = '第' + str(i) + '次训练/'
            trainBasicFile = basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
            testBasicFile = basicFilepath + projectFile + trainNumberFile + 'testCorpus/'

            """计算推荐标签"""
            trainWord = unicode(trainBasicFile +str(parameter) +'_1_trainCorpus_word.txt', 'utf-8')
            testWord = unicode(testBasicFile + str(parameter) +'_1_testCorpus_word.txt', 'utf-8')
            #
            newTrainTagFile = unicode(trainBasicFile + str(parameter) +'tag.txt', 'utf-8')
            recommendTagFile = unicode(testBasicFile + 'recommendTag1.txt', 'utf-8')
            print recommendTagFile
            timeConsumeFile = unicode(basicFilepath + projectFile + trainNumberFile + '推荐结果/' + 'TagMulRec_timeConsuming.txt', 'utf-8')
            """tagMulRec进行标签推荐"""
            # trainSentence = Corpus(trainWord)
            # testSentence = Corpus(testWord)
            #
            # trainDictionary = corpora.Dictionary(trainSentence)
            # t0 = time()
            # with open(recommendTagFile,'w') as e:
            #     for testText in testSentence:
            #     # wordSentenceNumberDict = TagMulRec.computeWSentenceDictInCorpus(trainSentence,trainDictionary.token2id.keys())
            #         wordSentenceNumberDict = {key:trainDictionary.dfs[trainDictionary.token2id[key]] for key in trainDictionary.token2id.keys()} ##效果一样
            #
            #         scoreDict = TagMulRec.computeScore(testText,trainSentence,wordSentenceNumberDict)
            #         maxValue, minValue = max(scoreDict.values()), min(scoreDict.values())
            #         # print scoreDict
            #         # for key in scoreDict:
            #         #         scoreDict[key] = (scoreDict[key] - minValue) / (maxValue - minValue)
            #
            #         e.write(json.dumps(TagMulRec.recommendTag(newTrainTagFile,scoreDict))+'\n')
            # t1 = time()
            # with open(timeConsumeFile,"w") as e:
            #     e.write(json.dumps([t1-t0]))

            """计算准确率"""
            if parameter == 3000:
                actualTagFile = unicode(testBasicFile +'tag.txt', 'utf-8')
            else:
                actualTagFile = unicode(testBasicFile + str(parameter) +'tag.txt', 'utf-8')
                recommendTagFile = unicode(testBasicFile + 'recommendTag1.txt', 'utf-8')
                resultExcel = unicode(basicFilepath + projectFile + trainNumberFile + '推荐结果/'+'TagMulRecRes.xls','utf-8')

            """计算每条pr的precision,recall,F1"""
            # outpath = unicode(basicFilepath + projectFile + trainNumberFile + '推荐结果/'+'TagMulRecRes_PerPR.csv','utf-8')
            # TagMulRec.computePercision_Recall_PerPR(recommendTagFile,actualTagFile,topKLs,outpath)

            """计算项目tagMulRec的precision,recall,F1"""
            # precesionDict, recallDict,F1Dict = TagMulRec.computePercision_Recall(recommendTagFile,actualTagFile,topKLs)
            # wb = Workbook()
            # sheet1 = wb.add_sheet('result',cell_overwrite_ok=True)
            # index = 0
            # sheet1.write(2, 0, 'tagMulRec')
            # for i in topKLs:
            #     sheet1.write(0, index+1, 'top'+str(i))
            #     sheet1.write(1, index+1, 'precision')
            #     sheet1.write(1, index+2, 'recall')
            #     sheet1.write(1, index+3, 'f1')
            #
            #
            #     sheet1.write(2, index+1, precesionDict[i])
            #     sheet1.write(2, index+2, recallDict[i])
            #     sheet1.write(2, index+3, F1Dict[i])
            #     index += 3
            # wb.save(resultExcel)
            #

            # """使用title plusdescription, filepath and contributor 作为corpus进行BPRec的推荐结果"""
            # for parameter in ['0.5','1','1.5']:
            #     BP_recommendTagFile = unicode(testBasicFile + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter) +'_BP_titlePlusDescribtion_recommend_tag.txt', 'utf-8')
            #     outpath = unicode(basicFilepath + projectFile + trainNumberFile+'推荐结果/' +str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter)+ '_Corpus_BPresult_PerPR.csv', 'utf-8')
            #     TagMulRec.BP_computePercision_Recall_PerPR(BP_recommendTagFile,actualTagFile,topKLs,outpath)
            #
            #     """计算BP的结果"""
            #     BP_resultExcel = unicode(basicFilepath + projectFile + trainNumberFile+'推荐结果/' +parameter+ '_Corpus_BPresult.xls', 'utf-8')
            #     precesionDict1, recallDict1, F1Dict1 = TagMulRec.BP_computePercision_Recall(BP_recommendTagFile, actualTagFile,topKLs)
            #     wb = Workbook()
            #     sheet1 = wb.add_sheet('result', cell_overwrite_ok=True)
            #     index = 0
            #     sheet1.write(2, 0, 'BPRec')
            #     for i in topKLs:
            #         sheet1.write(0, index + 1, 'top' + str(i))
            #         sheet1.write(1, index + 1, 'precision')
            #         sheet1.write(1, index + 2, 'recall')
            #         sheet1.write(1, index + 3, 'f1')
            #
            #         sheet1.write(2, index + 1, precesionDict1[i])
            #         sheet1.write(2, index + 2, recallDict1[i])
            #         sheet1.write(2, index + 3, F1Dict1[i])
            #         index += 3
            #     wb.save(BP_resultExcel)

            """使用2个月 title plusdescription, filepath and contributor 作为corpus进行BPRec的推荐结果"""
            # for parameter in ['0.5','1','1.5']:
            BP_recommendTagFile = unicode(testBasicFile + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter) +'_BP_allcorpus_recommend_tag.txt', 'utf-8')
            print(BP_recommendTagFile)
            outpath = unicode(basicFilepath + projectFile + trainNumberFile+'推荐结果/' +str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter)+ '_Corpus_BPresult_PerPR.csv', 'utf-8')
            try:
                TagMulRec.BP_computePercision_Recall_PerPR(BP_recommendTagFile,actualTagFile,topKLs,outpath)
            except Exception as e:
                print BP_recommendTagFile

            """计算BP的结果"""
            BP_resultExcel = unicode(basicFilepath + projectFile + trainNumberFile+'推荐结果/' +str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter) +'_BP_allcorpus_recommend_tag.xls', 'utf-8')
            precesionDict1, recallDict1, F1Dict1 = TagMulRec.BP_computePercision_Recall(BP_recommendTagFile, actualTagFile,topKLs)
            wb = Workbook()
            sheet1 = wb.add_sheet('result', cell_overwrite_ok=True)
            index = 0
            sheet1.write(2, 0, 'BPRec')
            for i in topKLs:
                sheet1.write(0, index + 1, 'top' + str(i))
                sheet1.write(1, index + 1, 'precision')
                sheet1.write(1, index + 2, 'recall')
                sheet1.write(1, index + 3, 'f1')

                sheet1.write(2, index + 1, precesionDict1[i])
                sheet1.write(2, index + 2, recallDict1[i])
                sheet1.write(2, index + 3, F1Dict1[i])
                index += 3
            wb.save(BP_resultExcel)

            """仅使用filepath作为corpus 计算BP的结果"""

            # BP_recommendTagFile = unicode(testBasicFile + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter) +'_BP_filepath_recommend_tag.txt', 'utf-8')
            # BP_resultExcel = unicode(basicFilepath + projectFile + trainNumberFile+'推荐结果/' +str(hiddenNeurons)+'_'  +str(epoch)+'_' +str(learning_rate) + '_' + str(parameter) +'filepath_BPresult.xls', 'utf-8')
            # precesionDict1, recallDict1, F1Dict1 = TagMulRec.BP_computePercision_Recall(BP_recommendTagFile, actualTagFile,topKLs)
            # wb = Workbook()
            # sheet1 = wb.add_sheet('result', cell_overwrite_ok=True)
            # index = 0
            # sheet1.write(2, 0, 'BPRec')
            # for i in topKLs:
            #     sheet1.write(0, index + 1, 'top' + str(i))
            #     sheet1.write(1, index + 1, 'precision')
            #     sheet1.write(1, index + 2, 'recall')
            #     sheet1.write(1, index + 3, 'f1')
            #
            #     sheet1.write(2, index + 1, precesionDict1[i])
            #     sheet1.write(2, index + 2, recallDict1[i])
            #     sheet1.write(2, index + 3, F1Dict1[i])
            #     index += 3
            # wb.save(BP_resultExcel)



