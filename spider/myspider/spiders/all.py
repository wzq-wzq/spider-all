import scrapy
from scrapy.utils.project import get_project_settings

import re
import datetime
from myspider.py_read.readcookie import get_cookies
from myspider.py_spiderneed.myre import mytime
from myspider.py_spiderneed.myre import mypercent

#from myspider.readjson import readfromsheet
from myspider.py_spiderneed.myjson import myjson

class AllSpider(scrapy.Spider):
    def __init__(self, sheet="",name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.sheet=sheet
        self.myjson=myjson(sheet=sheet)
    name = "all"
    allowed_domains = []

    
    #从设置中提取cookie
    cookie=get_cookies()

    #初始登录
    def start_requests(self):
        yield scrapy.Request(self.myjson.url,callback=self.parse,cookies=self.cookie)

    #处理页的方法
    def parse(self, response):
        #标题xpath
        node_list=response.xpath('')
        for node in node_list:
            node_text = node.xpath('').extract_first()
            flag=True
            #使用正则表达式表示是需要还是不需要关键词
            if re.search(self.myjson.titlekey,node_text):
                flag=self.myjson.titlekeyif
            else:
                flag=not self.myjson.titlekeyif
            if flag:
                try:
                    nowurl=node.xpath('./@href').extract_first()
                    print("nowurl:"+nowurl)
                    #进入对应链接
                    yield scrapy.Request(url=nowurl,callback=self.Mytest,cookies=self.cookie)
                except Exception as e:
                    print("error text:"+node_text)
            else:
                pass
        #翻页
        next_url=response.xpath('').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url,callback=self.parse,cookies=self.cookie)
    #处理单个子网页的方法
    def Mytest(self,response):
        temp={}
        #获取标题区文本，用来提取时间
        date_text=response.xpath('').extract_first()
        #myre.mytime是正则类中提取时间的对象，weeknum，date，time分别为年&周数，日期，时间
        try:
            a=mytime()
        except Exception as e:
            print(e)
        a.gettime(date_text)
        print("weeknum:"+a.weeknum)
        temp["年&周数"]=a.weeknum
        temp["日期"]=a.date
        temp["时间"]=a.time

        #提取一个个段落的文本
        node_list=response.xpath('')
        flag=True
        
        for node in node_list:
            node_text="".join(node.xpath('.//text()').extract())
            node_text="".join(node_text.split())
            print("段落:"+node_text)
            #段落标志词pkey对于一个sheet对应的子网页进行判断
            if(re.search(mypkey,node_text)):
                #如果找到，置标志flag为Fasle
                flag=False
                print("正确段落:"+node_text)
                #遍历此sheet中的要爬取的值的字典的列表
                for i in self.myjson.IndicsIDs:
                    if i["IndicsIDiftable"]=="yes":
                        continue
                    try:
                        a=mypercent()
                    except Exception as e:
                        print(e)
                    #三层正则获取数字
                    a.getpercent(node_text=node_text,fisrt_patterns=i["IndicsIDkey1"],second_patterns=i["IndicsIDkey2"],third_patterns=i["IndicsIDkey3"],len=i["len"])
                    mystr=a.percent
                    if mystr!="":
                        temp[i["IndicsID"]]=mystr
            
        
        #提交表格一行到pipeline下载
        yield temp
