#coding=utf-8

import json

class readFile():

    """
    读文件，返回二维list
    """
    @staticmethod
    def readFileToTDList(filepath):
        twoDimensionList = []
        with open(filepath,'r') as e:
            for line in e:
                twoDimensionList.append(json.loads(line))

    """
    将二维list写入文件中
    """