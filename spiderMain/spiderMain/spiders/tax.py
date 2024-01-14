from typing import Any, Optional
import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy import signals
from scrapy.signalmanager import dispatcher
from selenium import webdriver
from selenium.webdriver.common.by import By

from spiderMain.items import beijingItem, SpidermainItem


class TaxSpider(scrapy.Spider):
    name = "tax"
    # 通常不使用
    # allowed_domains = ["hd.chinatax.gov.cn"]
    # 默认，是北京的数据 # "http://beijing.chinatax.gov.cn/bjsat/office/jsp/zdsswfaj/wwquery.jsp",
    start_urls = {
        "天津":"https://tianjin.chinatax.gov.cn/wzcx/cx_zdwfaj.action?szsf=11200000000",
    }
                  

    def __init__(self, name: str | None = None, **kwargs: Any):
        super(TaxSpider, self).__init__(name, **kwargs)
        # 浏览器配置
        chrome_options = webdriver.ChromeOptions() # 实例化一个浏览器对象
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless') 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })
        self.driver.implicitly_wait(1) # 等待浏览器渲染
        dispatcher.connect(self.close_driver,signals.spider_closed)

    def start_requests(self):
        for url in self.start_urls:
            ### 1. 北京网页的处理
            if():
                self.driver.get(url)
                self.driver.find_element(By.XPATH, '//input[@id="zcdz"]').send_keys("北京")
                self.driver.find_element(By.XPATH,'//a[@onclick="dosearch()"]').click()
                self.driver.implicitly_wait(1) 
            ### 2. 天津网页的处理
            elif():
                self.driver.get(self.start_urls)
            ### 3. 广东网页的处理
            elif():
                self.driver.get()
            ### 4. 深圳网页的处理
            elif():
                self.driver.get
            # 获取当前页面的源代码
            page_source = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')
            # 调用parse方法处理响应
            yield Request(url=response.url, callback=self.parse)

    def beijingSearch(self, response:HtmlResponse):
        print('=====北京：parse(self, response)=====')
        # 获得结果
        # NOTE xpath中字符串内外引号不能相同
        print('测试response', response)
        case_list = response.xpath('//table[@width="700"]/table')
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
            # yield Request()

    def tianjinSearch(self, response):
        print('=====天津：parse(self, response)=====')
        # 获得结果
        case_list = response.xpath('//table[@class="table-update"]/tr')
        
    def guangdongSearch():
        pass

    def shenzhenSearch():
        pass

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
        # self.beijingSearch(response)
        self.tianjinSearch(response)

    def close_driver(self):
        print('爬虫已结束，正在关闭浏览器')
        self.driver.quit()