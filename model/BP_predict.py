#coding=utf-8

import torch
from torch.autograd import Variable

# from BP_text import computePrecession
import pandas as pd
from fileConfig.filepath import filepathConfig

# BPnet = torch.load('../model/BPnet.pkl')

test_xDF = pd.read_csv(filepathConfig.doc2bow_test)
test_yDF = pd.read_csv(filepathConfig.testTag_csv)
test_x,test_y = Variable(torch.FloatTensor(test_xDF.values)),Variable(torch.FloatTensor(test_yDF.values))

print(test_xDF.shape)
print(test_yDF.shape)


# test_out = BPnet(test_x)
# print '----------------result------------------'
# print computePrecession(test_out,test_y,5)