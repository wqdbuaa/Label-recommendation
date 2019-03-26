#coding=utf-8

class filepathConfig:

    trainPR = unicode(r'/media/mamile/DATA1/tagRecommendation_github/rails项目实验/第64次训练/trainCorpus/训练集.txt','utf-8')
    testPR = unicode(r'/media/mamile/DATA1/tagRecommendation_github/rails项目实验/第64次训练/testCorpus/测试集.txt','utf-8')

    trainFile = unicode(r'/media/mamile/DATA1/tagRecommendation_github/rails项目实验/第64次训练/trainCorpus/每个pr的word.txt','utf-8')
    testFile = unicode(r'/media/mamile/DATA1/tagRecommendation_github/rails项目实验/第64次训练/testCorpus/测试集中每个pr的word.txt','utf-8')
    corpus = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/corpusWord.txt','utf-8')

    wordDictionary = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/wordDictionary.txt','utf-8')
    new_trainFile = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/new_trainWord.txt','utf-8')
    new_testFile = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/new_testWord.txt','utf-8')
    new_corpus = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/new_corpusWord.txt','utf-8')

    trainTag = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/tag/trainTag.txt','utf-8')
    trainTag_csv = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/tag/trainTag.csv','utf-8')
    testTag = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/tag/testTag.txt','utf-8')
    testTag_csv = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/tag/testTag.csv','utf-8')

    doc2bow_train = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/doc2bow_train.csv','utf-8')
    doc2bow_test = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/doc2bow_test.csv','utf-8')

    excelpath = unicode(r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/第64次训练/BPresult.xls','utf-8')


    def __init__(self, projectName, index, hiddenNeurons=0.5, epoch=1000, learning_rate = 0.001, parameter=2000):
        # self.basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验/'
        self.basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(过滤训练集标签)/'
        #self.basicFilepath = r'/media/mamile/DATA1/tagRecommendation_github/BP_rails/10个项目的BP神经网络实验(2个月)/'

        projectFile = projectName + '项目实验/'
        trainNumberFile = '第' + str(index) + '次训练/'
        trainBasicFile = self.basicFilepath + projectFile + trainNumberFile + 'trainCorpus/'
        testBasicFile = self.basicFilepath + projectFile + trainNumberFile + 'testCorpus/'

        # if parameter != 3000:
        self.trainPR = unicode(trainBasicFile+str(parameter)+'tag.txt','utf-8')
        self.testPR = unicode(testBasicFile+str(parameter)+'tag.txt','utf-8')
        self.trainFile = unicode(trainBasicFile+str(parameter)+'_4_trainCorpus_word.txt','utf-8')
        self.testFile = unicode(testBasicFile+str(parameter)+'_4_testCorpus_word.txt','utf-8')
        # else:
        # self.trainPR = unicode(trainBasicFile + str(parameter)+'tag.txt', 'utf-8')
        # self.testPR = unicode(testBasicFile + str(parameter)+'tag.txt', 'utf-8')
        # self.trainFile = unicode(trainBasicFile +str(parameter)+ 'body_trainCorpus_word.txt', 'utf-8')
        # self.testFile = unicode(testBasicFile +str(parameter)+ 'body_testCorpus_word.txt', 'utf-8')
        #
        ###不变的变量
        self.corpus = unicode(self.basicFilepath + projectFile+trainNumberFile+'corpusWord.txt','utf-8')
        self.wordDictionary = unicode(self.basicFilepath + projectFile+trainNumberFile+'wordDictionary.txt','utf-8')
        # self.wordDictionary = unicode(self.basicFilepath + projectFile+trainNumberFile+'3wordDictionary.txt','utf-8')
        self.new_trainFile = unicode(trainBasicFile+'new_trainCorpus_word.txt','utf-8')
        self.new_testFile = unicode(testBasicFile+'new_testCorpus_word.txt','utf-8')
        self.new_corpus = unicode(self.basicFilepath + projectFile+trainNumberFile+'new_corpusWord.txt','utf-8')

        self.trainTag = unicode(trainBasicFile+'BPtag.txt','utf-8')
        self.trainTag_csv = unicode(trainBasicFile+'_BPtag.csv','utf-8')
        self.testTag = unicode(testBasicFile+'BPtag.txt','utf-8')
        self.testTag_csv = unicode(testBasicFile+'_BPtag.csv','utf-8')
        self.labelOccurrence_csv = unicode(trainBasicFile+'labelOccurrence.csv','utf-8')
        self.linkCreateTagOccurrenceNumber = unicode(trainBasicFile + '由链接产生的共现tag.txt', 'utf-8')
        self.linkPRNumber = unicode(trainBasicFile + '相互链接的pr的所有tag.txt', 'utf-8')
        self.PRNumberFile = unicode(self.basicFilepath + projectFile + 'pr编号.txt', 'utf-8')

        self.weightTag = unicode(trainBasicFile+'lastMonthTag.txt','utf-8')
        self.weightTag_csv = unicode(trainBasicFile+'lastMonthTag.csv','utf-8')

        self.doc2bow_train = unicode(trainBasicFile+'doc2bow_train.csv','utf-8')
        self.doc2bow_test = unicode(testBasicFile+'doc2bow_test.csv','utf-8')

        self.recommendFilepath = unicode(testBasicFile + str(hiddenNeurons) + '_' + str(epoch) + '_' + str(learning_rate) + '_' + str(parameter) + '_BP_allcorpus_recommend_tag.txt', 'utf-8')
        self.timeConsuming = unicode(self.basicFilepath + projectFile + trainNumberFile + '/推荐结果/'+str(parameter) +'contributor_timeCosuming.txt','utf-8')

        """考虑词语顺序的文本向量"""
        # self.doc2bow_train = unicode(trainBasicFile+'wordOrder_doc2bow_train.csv','utf-8')
        # self.doc2bow_test = unicode(testBasicFile+'wordOrder_doc2bow_test.csv','utf-8')

        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'BP.xls','utf-8')
        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'labelOccurrence_BPresult.xls','utf-8')
        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'sqrt_labelOccurrence_BPresult.xls','utf-8')
        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'lastMonth_labelOccurrence_BPresult.xls','utf-8')
        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'newCorpus_labelOccurrence_BPresult.xls','utf-8')
        self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'0.5_contributor_BPresult.xls','utf-8')
        # self.excelpath = unicode(self.basicFilepath + projectFile+trainNumberFile+'1_addLinkPRNumber_3_Corpus_BPresult.xls','utf-8')
        self.compareExcelPath = unicode(self.basicFilepath + projectFile+trainNumberFile+'tagMulRecRes.xls','utf-8')










