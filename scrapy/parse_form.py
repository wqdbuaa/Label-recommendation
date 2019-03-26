#coding=utf-8

import lxml.html
import pprint
import urllib2
import urllib
import cookielib
import json
import requests

def parse_form(html):
    tree = lxml.html.fromstring(html)
    data={}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

if __name__  == '__main__':
    user_file = unicode(r'H:\北航研究生学术论文\2017下半学期第三周(20170828-20170901)工作\20170901工作结果\更新用户设置label次数统计.txt', 'utf-8')
    user_list = []
    with open(user_file, 'r') as e:
        for line in e:
            tmpLs = json.loads(line)
            user_list.append(tmpLs)

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # print opener.addheaders

    Login_url = 'https://github.com/session'
    login_email = 'mambasmile'
    login_passwd = '930618caojin'

    loginhtml = opener.open(Login_url).read()
    # print html

    data = parse_form(loginhtml)
    # print data
    data['login']=login_email
    data['password'] = login_passwd

    tmp_data={}
    for k, v in data.iteritems():
        tmp_data[k] = unicode(v).encode('utf-8')

    # print tmp_data
    encoded_data = urllib.urlencode(tmp_data)
    # print encoded_data
    # encoded_data = json.dumps(tmp_data)

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        "Host":"github.com",
        "Origin":"https://github.com",
        "Referer":"https://github.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2924.87 Safari/537.36 LBBROWSER"
    }
    request = urllib2.Request(Login_url,encoded_data,headers)
    response = opener.open(request)

    template_url = 'https://github.com/'
    allUserEmail = []
    print user_list
    for pro_ls in user_list[2:]:
        user_email = []
        user_email.append(pro_ls[0])
        for val in pro_ls[1]:
            tmpLs=[val[0]]
            try:
                response = opener.open(template_url+val[0])
                sel = lxml.html.fromstring(response.read())
                email = sel.xpath('//*[@id="js-pjax-container"]/div/div[1]/ul/li[@aria-label="Email"]/a/text()')
                if email == []:
                    tmpLs.append(None)
                else:
                    tmpLs.append(email)

            except urllib2.HTTPError,e:
                tmpLs.append(None)
            user_email.append(tmpLs)
        allUserEmail.append(user_email)
    with open(unicode(r'H:\北航研究生学术论文\2017下半学期第四周(20170904-20170908)工作\1爬取用户email.txt','utf-8'),'a') as e:
        for ls in allUserEmail:
            e.write(json.dumps(ls)+'\n')


