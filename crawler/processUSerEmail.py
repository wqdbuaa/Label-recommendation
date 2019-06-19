#coding=utf8

import json
import xlwt

emailfile = unicode(r'H:\北航研究生学术论文\2017下半学期第四周(20170904-20170908)工作\爬取用户email.txt','utf-8')
userLabel = unicode(r'H:\北航研究生学术论文\2017下半学期第三周(20170828-20170901)工作\20170901工作结果\更新用户设置label次数统计.txt','utf-8')
outpath = unicode(r'H:\北航研究生学术论文\2017下半学期第四周(20170904-20170908)工作\用户email以及label次数.txt','utf-8')

# user_email = {}
# count=0
# with open(emailfile,'r') as e:
#     for line in e:
#         data = json.loads(line)
#         for val in data:
#             if isinstance(val,list):
#                 if val[1] == None:
#                     user_email[val[0]] = None
#                 else:
#                     user_email[val[0]] = val[1][0]
#                     count+=1
# print count

# print user_email.__len__()

# with open(outpath,'w') as e:
#     with open(userLabel,'r') as e1:
#         for line in e1:
#             tmpLs = []
#             data = json.loads(line)
#             tmpLs.append(data[0])
#             for val in data[1]:
#                 ls = val
#                 try:
#                     ls.append(user_email[val[0]])
#                 except KeyError,e:
#                     print data
#                     print val
#                     break
#                 tmpLs.append(ls)
#             e.write(json.dumps(tmpLs)+'\n')

wb = xlwt.Workbook()
sheet1 = wb.add_sheet(u'用户email')
sheet1.write(0,0,'userName')
sheet1.write(0,1,'repo')
sheet1.write(0,2,'labelCounts')
sheet1.write(0,3,'email')
lineNum=1
with open(outpath,'r') as e:
    for line in e:
        data = json.loads(line)
        repo = data[0].split(',')[1]
        for val in data[1:]:
            sheet1.write(lineNum,0,val[0])
            sheet1.write(lineNum,1,repo)
            sheet1.write(lineNum,2,val[1])
            sheet1.write(lineNum,3,val[2])
            lineNum+=1
wb.save(unicode(r'H:\北航研究生学术论文\2017下半学期第四周(20170904-20170908)工作\用户email以及label次数.xls','utf-8'))
