import scrapy
from typing import Any, Optional
from scrapy.http import Request, HtmlResponse
from scrapy import Selector

from spiderMain.items import beijingItem,shenzhenItem

class TaxSpider(scrapy.Spider):
    name = "tax"
    # 通常不使用
    # allowed_domains = ["hd.chinatax.gov.cn"]
    cities_urls = {
        "天津": "https://tianjin.chinatax.gov.cn/wzcx/cx_zdwfaj.action?szsf=11200000000",
        "北京": "http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp",
        "广东": "https://guangdong.chinatax.gov.cn/siteapps/webpage/gdtax/zdsswfaj/index.jsp",
        "深圳": "https://shenzhen.chinatax.gov.cn/sztaxapp/zdsswfaj/index"
    }
    current_page = 0
    def start_requests(self):
        for location, url in self.cities_urls.items():
            yield Request(url=url, callback=self.parse, meta={'location':location, 'next_page':False})        
            
    def parse(self, response):
        location = response.meta.get('location', None)
        if(location=='北京'):
            self.current_page += 1
            print('=====北京：parse(self, response)=====')
            # 获得结果
            # NOTE xpath中字符串内外引号不能相同
            new_page = response.body
            case_list = Selector(text=new_page).xpath('/html/body/table/tbody/tr')
            case_list = case_list[1:-1]
            for case in case_list:
                item = beijingItem()
                item_string_list = case.xpath('string(.)').extract() # 返回的是list
                item_list = "".join(item_string_list).split('\n')
                print('\n\n去喵喵',item_list)
                tmp = []
                for i in range(2, len(item_list)-2):
                    tmp.append(item_list[i].strip().replace('\t\t\t\t\t', '')) 
                item['area'] = '北京'
                item['location'] = tmp[0]
                item['company'] = tmp[1]
                item['id'] = tmp[2]
                item['lawCase'] = tmp[3]
                print('\n\n看我看我',tmp)
                yield item
            if self.current_page < 167:
                yield Request(url=response.url, callback=self.parse, meta={'location':'北京','next_page':True},dont_filter=True)
            else:
                self.current_page = 0
        elif(location=='天津'):
            print('=====天津：parse(self, response)=====')
            # 获得结果
            new_page = response.body # NOTE 由于new_page是字符串，后续需要使用Selector处理才能使用xpath
            case_list = Selector(text=new_page).xpath('/html/body/div[1]/table[1]/tbody/tr/td/table/tbody/tr')
            case_list = case_list[1:-1] # 删除第一行表头和最后一行长度为0的
            for case in case_list:
                # 将数据封装到SpidermainItem对象，这边和北京的一致
                item = beijingItem()
                item_string_list = case.xpath('string(.)').extract() # 返回的是list
                item_string = "".join(item_string_list) # 将list转为string
                item_list = item_string.split('\n')
                tmp = []
                for i in range(1, len(item_list)-2):
                    tmp.append(item_list[i].strip().replace('\xa0', '')) #strip()去除空白字符，replace('\xa0', '')用于去除\xa0字符
                
                item['area'] = '天津'
                item['location'] = tmp[0]
                item['company'] = tmp[1]
                item['id'] = tmp[2]
                item['lawCase'] = tmp[3]

                yield item # NOTE item要放在parse()方法中，如果放在其他函数如tianjinSearch(self, response)则无法返回parse的上下文
            
            # 如果还有下一页，则继续翻页: dont_fillter=True表示不过滤重复的请求。
            yield Request(url=response.url, callback=self.parse, meta={'location':'天津','next_page':True},dont_filter=True)

        elif(location=='广东'):
            self.current_page += 1
            new_page = response.body
            print('=====广东：parse(self, response)=====')
            case_list = Selector(text=new_page).xpath('/html/body/div[1]/table[1]/tbody/tr/td/table/tbody/tr')
            case_list = case_list[1:-1] 
            tmp = []
            for case in case_list:
                item = shenzhenItem()
                item_string_list = case.xpath('string(.)').extract()
                item_string = "".join(item_string_list)
                item_list = item_string.split('\n')
                for i in range(1, len(item_list)-2):
                    tmp.append(item_list[i].strip().replace('\xa0', ''))

                item['area'] = '广东'
                item['location'] = tmp[0]
                item['company'] = tmp[1]
                item['id'] = tmp[2]
                item['lawCase'] = tmp[3]
                item['time'] = tmp[4]

            if self.current_page< 526:
                yield Request(url=response.url, callback=self.parse, meta={'location':'广东','next_page':True, 'next_page_detail':self.current_page+1},dont_filter=True)
            else:
                self.current_page = 0

        elif(location=='深圳'):
            print('=====深圳：parse(self, response)=====')
            case_list = Selector(text=new_page).xpath('/html/body/div[1]/table[1]/tbody/tr/td/table/tbody/tr')
            case_list = case_list[1:-1] 
            for case in case_list:
                item = shenzhenItem()
                item_string_list = case.xpath('string(.)').extract()
                item_string = "".join(item_string_list)
                item_list = item_string.split('\n')
                for i in range(1, len(item_list)-2):
                    tmp.append(item_list[i].strip().replace('\xa0', '')),
                item['area'] = '深圳'
                item['location'] = tmp[0]
                item['company'] = tmp[1]
                item['id'] = tmp[2]
                item['lawCase'] = tmp[3]
                item['time'] = tmp[4]
                
            yield Request(url=response.url, callback=self.parse, meta={'location':'深圳','next_page':True})
            
    def close_driver(self):
        print('爬虫已结束，正在关闭浏览器')