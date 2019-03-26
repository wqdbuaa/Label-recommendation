#coding=utf-8

import json

class prFilter():
    @staticmethod
    def filterPR(filepath1,filepath2,destinationFilepath):
        with open(filepath1,'r') as e:
            with open(filepath2,'r') as e1:
                pass

    def process(self):
        with open(r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\leftPRCloseTime.txt', 'r') as e:
            with open(r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\allPRLabelTime.txt',
                      'w') as e1:
                with open(r'E:\beihang_study\mypaper\tagRecommendationExperiment\experiment1\prLabelTime.txt',
                          'r') as e2:
                    index = 0
                    for line in e2:
                        data = json.loads(line)
                        if data.__len__() > 3:
                            e1.write(json.dumps(data) + '\n')
                            e1.flush()
                        else:
                            for lines in e:
                                tmpData = json.loads(lines)
                                if tmpData.__len__() == 3:
                                    break
                                else:
                                    if tmpData[0] == data[0] and tmpData[1] == data[1] and tmpData[2] == data[2]:
                                        data.extend(tmpData[3:])
                            e1.write(json.dumps(data) + '\n')
                            e1.flush()