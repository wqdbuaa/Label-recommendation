#coding=utf-8

import re

class dateCompare:

    """
       比较日期的大小，
       model=0，date1 >= date2 返回True
       model=1，date1 =< date2 返回True
       model=2，date1 < date2 返回True ;严格小于

       """

    @classmethod
    def dateCompareto(cls,date1, date2, mode):
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
                tmpTime1 = int("".join(date1[3:]))
                tmpTime2 = int("".join(date2[3:]))
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
                tmpTime1 = int("".join(date2[3:]))
                tmpTime2 = int("".join(date1[3:]))
                if tmpTime1 >= tmpTime2:
                    return True
                else:
                    return False
        elif mode == 2:
            tmpDate1 = int("".join(date2[:3]))
            tmpDate2 = int("".join(date1[:3]))
            if tmpDate1 < tmpDate2:
                return False
            elif tmpDate1 > tmpDate2:
                return True
            else:
                tmpTime1 = int("".join(date2[3:]))
                tmpTime2 = int("".join(date1[3:]))
                if tmpTime1 > tmpTime2:
                    return True
                else:
                    return False

    """
    求时间差值
    """
    @classmethod
    def calSubTime(cls,date1,date2):
        date1 = re.sub("[-T:Z]", " ", date1).strip().split(" ")
        date2 = re.sub("[-T:Z]", " ", date2).strip().split(" ")
        # print date1,date2
        date1Year = int(date1[0])
        date2Year = int(date2[0])
        date1Mth = int(date1[1])
        date2Mth = int(date2[1])
        day1 = int(date1[3])*3600+int(date1[4])*60+int(date1[-1])
        day2 = int(date2[3])*3600+int(date2[4])*60+int(date2[-1])
        daySum1 = dateCompare.sumDays([date1Year,date1Year],date1Mth)+int(date1[2])
        daySum2 = dateCompare.sumDays([date1Year,date2Year],date2Mth)+int(date2[2])
        # print day1,day2
        # print dateCompare.sumHour(day2,day1)
        # print daySum2-daySum1
        return daySum2-daySum1+dateCompare.sumHour(day2,day1)

    @classmethod
    def retMonthDays(cls,year,month):
        if month in [1,3,5,7,8,10,12]:
            return 31
        elif month in [4,6,9,11]:
            return 30
        else:
            if year % 100 == 0:
                if year % 400 == 0:
                    return 29
                else:
                    return 28
            elif year % 4 == 0:
                return 29
            else:
                return 28

    @classmethod
    def retYearDays(cls,year):
        if year % 100 == 0:
            if year % 400 == 0:
                return 366
            else:
                return 365
        elif year % 4 == 0:
            return 366
        else:
            return 365

    """
    传入年段,月份
    """
    @classmethod
    def sumDays(cls,yearLs,month):
        # print yearLs
        ret = 0
        for ele in range(yearLs[0],yearLs[1]):
            ret+=dateCompare.retYearDays(ele)
        # print ret
        for ele in range(1,month):
            ret+=dateCompare.retMonthDays(yearLs[-1],ele)
        return ret

    """传入小时、分钟"""
    @classmethod
    def sumHour(cls,day1,day2):
        return (day1-day2)/86400.0

    @classmethod
    def timeSumMonth(cls,date,monthNum):
        res = date.split('T')
        oldDate = res[0].split('-')
        newMonthRes = int(oldDate[1])+monthNum
        if newMonthRes<=0:
            newMonthRes += 12
            if newMonthRes < 10:
                date = "-".join([str(int(oldDate[0]) - 1), '0' + str(newMonthRes), oldDate[2]])
            else:
                date = "-".join([str(int(oldDate[0]) - 1), str(newMonthRes), oldDate[2]])
        else:
            if newMonthRes>12:
                monthRes = newMonthRes-12
                if monthRes<10:
                    date = "-".join([str(int(oldDate[0]) + 1), '0'+str(monthRes), oldDate[2]])
                else:
                    date = "-".join([str(int(oldDate[0]) + 1), str(monthRes), oldDate[2]])
            if newMonthRes <= 12:
                if newMonthRes>=10:
                    date = "-".join([str(int(oldDate[0])),str(newMonthRes),oldDate[2]])
                else:
                    date = "-".join([oldDate[0], str(0) + str(newMonthRes), oldDate[2]])

        return "T".join([date,res[1]])

    """计算中位数以及平均数"""
    @classmethod
    def computeAvgAndMid(cls,tmpLs):
        if tmpLs.__len__() == 0:
            return 0,0
        else:
            tmpLs = sorted(tmpLs)
            avg = sum(tmpLs) / float(len(tmpLs))
            if tmpLs.__len__() % 2 == 0:
                mid = (tmpLs[tmpLs.__len__() / 2 - 1] + tmpLs[tmpLs.__len__() / 2]) / 2.0
            else:
                mid = tmpLs[tmpLs.__len__() / 2]
            return avg,mid

if __name__ == '__main__':
    # print dateCompare.dateCompareto('2012-01-09T18:18:24Z','2012-01-09T18:18:24Z',2)
    # print re.sub("[-T:Z]", " ", '2012-01-09T18:18:24Z').strip().split(" ")
    # print dateCompare.timeSumMonth('2016-11-17T07:46:28Z',1)
    # # print dateCompare.sumDays([2016,2017],2)
    # print sum([366,365,365,365,31,29,31,30,31,2])
    # print sorted([1,2,3,4,5,5,-1])
    print dateCompare.computeAvgAndMid([1,2,4,-1,9,2])