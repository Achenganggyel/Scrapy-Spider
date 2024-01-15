# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from typing import Any
from scrapy.http import HtmlResponse
from scrapy import signals, Selector
from scrapy.signalmanager import dispatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SpidermainSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SpidermainDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# selenium
class SeleniumDownloaderMiddleware:
    def __init__(self):
        # 浏览器配置
        chrome_options = webdriver.ChromeOptions() # 实例化一个浏览器对象
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument("--disable-images")  # 禁用加载图片
        chrome_options.add_argument("--disable-extensions")  # 禁用加载扩展程序
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless') # 无头模式，不显示界面，可加快速度
        self.driver = webdriver.Chrome(options=chrome_options) # NOTE Selenium 4中无需显式指定executable_path参数
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
        })
        self.driver.implicitly_wait(1) # 等待浏览器渲染
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
    
    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s" % spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        #下面这一行需要手动添加，作用是调用关闭浏览器的函数
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    
    def process_request(self, request, spider):
        self.driver.get(request.url)
        print(f"当前访问{request.url}")
        location = request.meta.get('location', None)
        ### 1. 北京网页的处理
        if(location=='北京'):
            next_btn_html = "/html/body/table/tbody/tr/td/table[2]/tbody/tr[11]/td[3]/span/a[2]"
            # 如果传入点击下一页
            if(request.meta.get('next_page', None)):
                selector = Selector(text=self.fisrt_Page)
                elements = selector.xpath(next_btn_html)
            else:
                self.driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr[1]/td[3]/form/table/tbody/tr/td/table[2]/tbody/tr/td[2]/input').send_keys("北京")
                self.driver.find_element(By.XPATH,'/html/body/div[1]/table/tbody/tr[1]/td[3]/form/table/tbody/tr/td/table[5]/tbody/tr/td[3]/a').click()
                wait = WebDriverWait(self.driver, 15)
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/iframe")) 
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/table'))) # 显式等待
                self.fisrt_Page = self.driver.execute_script("return document.body.innerHTML;")
        
        ### 2. 天津网页的处理
        elif(location=='天津'):
            next_btn_html = "//li[@id='next' and not(@class)]"
            # 如果传入点击下一页
            if(request.meta.get('next_page', None)):
                selector = Selector(text=self.fisrt_Page)
                elements = selector.xpath(next_btn_html)
                if elements:
                    next_btn = self.driver.find_elements(By.XPATH, next_btn_html)
                    if next_btn:
                        next_btn[0].click()
                else:
                    return
            else: # 进入第一页
                self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/table/tbody/tr[3]/td").click()
                wait = WebDriverWait(self.driver, 15)
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/iframe")) 
                test = EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/table[1]/tbody/tr/td/table"))
                wait.until(test)
                self.fisrt_Page = self.driver.execute_script("return document.body.innerHTML;")
                
        ### 3. 广东网页的处理
        elif(location=='广东'):
            # 如果传入点击下一页
            if(request.meta.get('next_page', None)):
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[2]/span[11]/input').send_keys(request.meta.get('next_page_detail', None))
                self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[2]/span[11]/a').click()
            else: # 进入第一页
                self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/h2[1]").click()
                wait = WebDriverWait(self.driver, 15)
                test = EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[1]/table"))
                wait.until(test)
                self.fisrt_Page = self.driver.execute_script("return document.body.innerHTML;")
        
        ### 4. 深圳网页的处理
        elif(location=='深圳'):
            next_btn_html = '/html/body/div/form/table[2]/tbody/tr/td/a[3]'
            # 如果传入点击下一页
            if(request.meta.get('next_page', None)):
                selector = Selector(text=self.fisrt_Page)
                elements = selector.xpath(next_btn_html)
                if elements:
                    next_btn = self.driver.find_elements(By.XPATH, next_btn_html)
                    if next_btn:
                        next_btn[0].click()
                else:
                    return
            else: # 进入第一页
                self.driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[3]/table[1]/tbody/tr/td/form/table[2]/tbody/tr/td[2]/input").send_keys('深圳')
                self.driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[3]/table[1]/tbody/tr/td/form/table[4]/tbody/tr/td[3]/a/span").click()
                wait = WebDriverWait(self.driver, 15)
                self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[3]/table[2]/tbody/tr[2]/td/iframe")) 
                test = EC.visibility_of_element_located((By.XPATH, "/html/body/div/form/table[1]"))
                wait.until(test)
                self.fisrt_Page = self.driver.execute_script("return document.body.innerHTML;")

        # 获取当前页面的源代码：不能刷新！
        # page_source = self.driver.page_source
        self.page_source = self.driver.execute_script("return document.body.innerHTML;")  
        return HtmlResponse(url=self.driver.current_url, body=self.page_source, encoding='utf-8') # NOTE Request可以加入meta，htmlResponse不可以
    
    def process_response(self, request, response, spider):
        return response
    
# 多主机模拟
class RandomUserAgentMiddleware(object):
    def __init__(self, user_agents) -> None:
        self.user_agents = user_agents
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.user_agents))