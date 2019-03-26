#coding=utf-8

import bs4
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.item import Item,Field
from scrapy.http import Request,FormRequest
import urllib
from urllib import urlopen
import urllib2
import cookielib
import re
import logging
# from scrapy import log

class GitHubSpider(Spider):
    """爬取GitHub数据"""
    name="githubspider"
    allowed_domains=["github.com"]
    # start_url=["https://github.com/login",]
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.2924.87 Safari/537.36 LBBROWSER",
    "Referer": "https://github.com"
    }

    def start_requests(self):
        return [Request("https://github.com/session", meta = {'cookiejar' : 1}, callback = self.post_login)]
    #当我们单个spider中每次只有一个request时候，因为默认是使用一个cookiejar来处理，
    # 所以我们在发出request的时候，不需要手动使用meta来给它布置cookiejar，
    # 但是当单个spider多个request的时候，因为返回的每个response要求下一个request带的cookie都不同，
    # 所以每一次都要手动给每个request添加cookiejar来记录

    def post_login(self, response):
        print 'Preparing login'
        #下面这句话用于抓取请求网页后返回网页中的authenticity_token字段的文字, 用于成功提交表单
        authenticity_token = Selector(response).xpath('//meta[@name="csrf-token"]/@content').extract()[0]
            #authenticity_token = Selector(response).xpath('text()').re(r'\w*?=\"(\w*?\/\w*?\/\w*?==)\"').extract()[1]
        #正则表达式匹配的是authenticity_token值
        print "authenticity_token:"
        print authenticity_token
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,

                                          meta = {'cookiejar' : response.meta['cookiejar']},
                                          headers = self.headers,  #注意此处的headers
                                          formdata = {
                                                  'authenticity_token': authenticity_token,
                                                  'login': '13277061183@163.com',
                                                  'password': '930618caojin'
                                                  },
                                          callback = self.parse_page,
                                          dont_filter = True,
                                          formnumber=1
                                          )]
    #def after_login(self, response) :
        #for url in self.start_urls :
            #yield self.make_requests_from_url(url)

    def parse_page(self,response):
        self.log("login.....")
        webdata=response.body
        output=open("mygithub.html","w")
        output.write(webdata)
        output.close()
        if not "Z0fr3y" in response.body:
            self.log("login failed!!!!",level=logging.ERROR)
            return
        self.log("login success!!!!")
        title=[]
        sel=Selector(response)
        title=sel.xpath('//title/text()').extract()[0]
        #user=sel.xpath('//meta[@name="user-login"]/@content').extract()[0]
        user=sel.xpath('//div[@class="dropdown-header header-nav-current-user css-truncate"]/strong/text()').extract()
        print "user:"
        print user
        print "title:"
        print title
