# coding=utf-8
'''
Created on 2017年5月15日

@author: Administrator
'''
from handleCorpus import *


# from src.computeO2O import allRecommendTags

class computePrecision():
    @staticmethod
    def computePrecis(recommendTag, actualTag, k):
        commonTag = 0
        for tag in recommendTag:
            if tag in actualTag:
                commonTag += 1
        L = len(actualTag) - 1
        if L > k:
            return float(commonTag) / k
        else:
            return float(commonTag) / L

    @staticmethod
    def computeAveragePrecis(allPrecis, testObjectNum):
        return float(sum(allPrecis)) / testObjectNum


if __name__ == '__main__':
    allRecommendTags = []
    filepath1 = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpu\exper1\allRecommendTag.txt'
    with open(filepath1, 'r') as e:
        for line in e:
            allRecommendTags.append(json.loads(line))
    print len(allRecommendTags)
    allActualTags = []
    allPrecis = []
    filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpu\testCorpus.txt'
    allActualTags = getCorpus.getObjectTag(filepath)
    #     print allActualTags
    for i in range(len(allActualTags)):
        allPrecis.append(computePrecision.computePrecis(allRecommendTags[i], allActualTags[i], 5))
    print len(allPrecis)
    print computePrecision.computeAveragePrecis(allPrecis, len(allRecommendTags))
