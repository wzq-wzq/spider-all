# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pandas as pd
from openpyxl import load_workbook
#由spider运行,import从myspide开始
from myspider.py_excel.mytest import join_excel
class MyspiderPipeline(object):
    def open_spider(self,spider) :
        #修改list
        list=['日期','时间']
        self.df=pd.DataFrame(columns=list)
    def process_item(self, item, spider):
        try:
            #把yield的字典添加到数据中
            series = pd.Series(item)
            self.df=self.df.append(series, ignore_index=True)
        except Exception as e:
            print(e)
        return item
    def close_spider(self,spider):
        #修改filename
        filename=""
        with pd.ExcelWriter(filename,mode='a',engine='openpyxl',if_sheet_exists="replace") as writer:
            self.df.to_excel(writer,sheet_name=spider.sheet,index=False)

        



