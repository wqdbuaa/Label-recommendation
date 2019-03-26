# coding=utf-8
'''
Created on 2017��5��9��

@author: Administrator
'''
import json
import re


# mydict = "2017-05-06T19:16:48Z"
# mydict = re.sub("[-T:Z]", " ",mydict).strip().split(" ")
# print mydict
# m=re.findall("[^abc]","asdfabbbb")
# print m
# m=re.findall("[^a\w+]","abcdfa\na1b2c3",re.MULTILINE)
# print m

class dataHandle():
    trainCorpus_filepath = r"E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1\trainCorpus.txt"

    """
    过滤数据
    2017-01-01T00:00:00Z
    2017-04-01T00:00:00Z
    """

    @staticmethod
    def filterData(filepath, createDate, closedDate):
        with open(filepath, "w") as e1:
            with open(r"E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\pullrequest.txt", "r") as e:
                for line in e:
                    corpus = {}
                    data = json.loads(line)
                    #                 print data['userName']
                    if data["labelFlag"] == True:
                        #                     print 'smile'
                        if dataHandle.dateCompareto(createDate, data["created_at"], 1) and dataHandle.dateCompareto(
                                closedDate, data["closed_at"], 0):
                            #                         corpus["title"] = data["title"]
                            #                         corpus["body"] = data["body"]
                            #                         corpus["respOwner"] = data["userName"]
                            #                         corpus["respName"] = data["body"]
                            #                         corpus["label"] = data["labelName"]
                            #                         corpus["number"]= data["number"]
                            #                         corpus["userName"]=data["userName"]
                            #                         corpus["userId"]=data["userId"]
                            e1.write(json.dumps(data) + "\n")
                e1.flush()

    """
    比较日期的大小，
    model=0，date1 >= date2 返回True
    model=1，date1 =< date2 返回True
    """

    @staticmethod
    def dateCompareto(date1, date2, mode):
        date1 = re.sub("[-T:Z]", " ", date1).strip().split(" ")
        date2 = re.sub("[-T:Z]", " ", date2).strip().split(" ")
        if mode == 0:
            tmpDate1 = int("".join(date1[:3]))
            tmpDate2 = int("".join(date2[:3]))
            if tmpDate1 < tmpDate2:
                return False
            elif tmpDate1 > tmpDate2:
                return True
            else:
                tmpTime1 = int("".join(date1[3:-1]))
                tmpTime2 = int("".join(date2[3:-1]))
                if tmpTime1 >= tmpTime2:
                    return True
                else:
                    return False
        elif mode == 1:
            tmpDate1 = int("".join(date2[:3]))
            tmpDate2 = int("".join(date1[:3]))
            if tmpDate1 < tmpDate2:
                return False
            elif tmpDate1 > tmpDate2:
                return True
            else:
                tmpTime1 = int("".join(date2[3:-1]))
                tmpTime2 = int("".join(date1[3:-1]))
                if tmpTime1 >= tmpTime2:
                    return True
                else:
                    return False

    """
    得到pull request与号码之间的映射关系
    filepath1:源文件夹
    filepath2:目标文件夹
    """

    @staticmethod
    def saveNumbertoFile(filepath1, filepath2):
        with open(filepath2, "w") as e:
            with open(filepath1, "r") as e1:
                counter = 0
                for line in e1:
                    tmpdata = {}
                    data = json.loads(line)
                    tmpdata[counter] = data.get('number')
                    counter += 1
                    e.write(json.dumps(tmpdata) + '\n')
            e.flush()

    """
    筛选出所有pull request的关闭时间，得到[owner，repository，number，closeTime]
    """
    @staticmethod
    def getPRCloseTime(filepath1,filepath2):
        with open(filepath1,'w') as e:
            with open(filepath2,'r') as e1:
                for line in e1:
                    data = json.loads(line)
                    if data['labelFlag'] == False:
                        continue
                    tmplist = [data['owner'], data['respName'], data['number'], data['closed_at']]
                    e.write(json.dumps(tmplist)+'\n')
            e.flush()

    """
    筛选出测试集和训练集中使用的pull request对应的用户名与仓库名,以及pull request的数目
    """
    @staticmethod
    def getPrSetDetailInformation():
        filepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpu\testCorpus.txt'
        with open(r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\firstTrainSet\testCorpusSet.txt',
                  'w') as e1:
            with open(filepath, 'r') as e:
                currentrespName = ''
                currentOwner = ''
                flag = False

                for line in e:
                    data = json.loads(line)
                    if not flag:
                        currentrespName = data['respName']
                        currentOwner = data['owner']
                        count = 1
                        flag = True
                    else:
                        if (data['respName'] == currentrespName) and (data['owner'] == currentOwner):
                            count += 1
                        else:
                            # print '--'
                            e1.write(currentOwner + ',' + currentrespName + ',' + str(count) + '\n')
                            e1.flush()
                            currentrespName = data['respName']
                            currentOwner = data['owner']
                            count = 1
                e1.write(currentOwner + ',' + currentrespName + ',' + str(count) + '\n')
                e1.flush()

    """
    筛选数据，根据pull request的closeTime和label的creatTime
    """
    @staticmethod
    def filterDataCompareTime():
        pass


def main():
    #     filterData("2017-01-01T00:00:00Z","2017-04-01T00:00:00Z")
    #     filepath1 = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus\trainCorpus.txt'
    #     filepath2 = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\middleRes\corpusNumber.txt'
    filepath1 = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1\trainCorpus.txt'
    filepath2 = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\corpus1'
    tmpPath = r'\exper1'
    endPath = r'\corpusNumber.txt'
    filepath2 = filepath2 + tmpPath + endPath
    #     print filepath2
    #     dataHandle.filterData(dataHandle.trainCorpus_filepath, "2016-04-01T00:00:00Z", "2017-04-01T00:00:00Z")

    dataHandle.saveNumbertoFile(filepath1, filepath2)
    pullrequestFilepath = r'E:\beihang_study\scapy_spider\githubPullRequest\prclosedLabel\pullrequest.txt'
    pullrequestCloseTimeFilepath = r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\prCloseTime.txt'
    dataHandle.getPRCloseTime(pullrequestCloseTimeFilepath,pullrequestFilepath)
    # prList = []
    # with open(r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\prCloseTime1.txt', 'r') as e:
    #     for line in e:
    #         prList.append(json.loads(line))
    # print prList

if __name__ == '__main__':
    main()