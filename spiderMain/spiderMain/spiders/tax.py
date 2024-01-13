from typing import Iterable
import scrapy
from scrapy.http import Request, FormRequest
from spiderMain.items import beijingItem, SpidermainItem

class getFormModel():
    pass

class TaxSpider(scrapy.Spider):
    name = "tax"
    # 通常不使用
    # allowed_domains = ["hd.chinatax.gov.cn"]
    # 不同城市的URL，由于案件信息只能通过在
    cities_urls = ["http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp"]
    # 默认，是北京的数据
    start_urls = [cities_urls[0]]

    def start_requests(self):
        # search_address = "北京" # 搜索条件：注册地址
        # # 进行搜索和URL抓取：将地点和网站相对应
        # submit_btn = ('//a[@href and @onclick]')
        # formdata = {
        #     ''
        # }
        # yield FormRequest()
        request = scrapy.FormRequest("http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp",
                formdata={
                    'nsrmc': '',
                    'nsrsbh': '',
                    'zcdz': '北京',
                    'nsrmc': '',
                    'zzjgdm': '',
                    'fddbrmc': '',
                    'fddbrsfzhm': '',
                    'cwfzrmc': '',
                    'cwfzrsfzhm': ''
                },callback=self.parse)
        yield request

    def beijingSearch(self, response):
        print('=====北京：parse(self, response)=====')
        # 获得结果
        # NOTE xpath中字符串内外引号不能相同
        print('测试', response)
        case_list = response.xpath('(//table[@width="700"]/table)[2]/tr')
        print('未处理的数据', case_list)
        res = []
        for case in case_list:
            # 将数据封装到SpidermainItem对象
            item = beijingItem()
            # extract()法返回的都是unicode字符串，xpath返回的是包含一个元素的列表、用于进行HTML代码解析
            item_string_list = case.xpath('string(.)').extract() # 返回的是list
            # 返回数据
            item['location'] = item_string_list[0]
            item['company'] = item_string_list[1]
            item['id'] = item_string_list[2]
            item['lawCase'] = item_string_list[3]
            print('数据列表\n',item_string_list,'处理后的数据\n', item)
            res.append(item)

        print('我的数据呢?', res)
            # yield Request()

    # https://tianjin.chinatax.gov.cn/wzcx/cx_zdwfaj.action?szsf=11200000000
    def tianjinSearch(self, response):
        print('=====天津：parse(self, response)=====')
        # 获得结果
        case_list = response.xpath('//table[@class="table-update"]/tr')

    # def guangdongSearch():
    #     pass

    # def shenzhenSearch():
        
    #     pass
    def detail(case_list):
        for case in case_list:
            item = SpidermainItem()
            item['company'] = case.xpath('').extract()[0].strip()
            item['id'] = case.xpath('').extract()[0]
            item['address'] = case.xpath('').extract()[0]
            item['referees'] = case.xpath('').extract()[0]
            item['refereesInBreakLaws'] = case.xpath('').extract()[0]
            item['directInBreakLaws'] = case.xpath('').extract()[0]
            item['realInBreakLaws'] = case.xpath('').extract()[0]
            item['agencyInBreakLaws'] = case.xpath('').extract()[0]
            item['lawCase'] = case.xpath('').extract()[0]
            item['punish'] = case.xpath('').extract()[0]
            
    def parse(self, response):   
        self.beijingSearch(response)