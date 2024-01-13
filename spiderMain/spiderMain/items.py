# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class beijingItem(scrapy.Item):
    # 所属税务机关名称
    location = scrapy.Field()
    # 失信主体
    company = scrapy.Field()
    # 识别号
    id = scrapy.Field()
    # 违法性质
    lawCase = scrapy.Field() 

# 详细的信息
class SpidermainItem(scrapy.Item):
    # define the fields for your item here like:
    # 纳税人名称
    company = scrapy.Field()
    # 纳税人识别号或信用代码
    id = scrapy.Field()
    # 注册地址
    address = scrapy.Field()
    # 法定代表人
    referees = scrapy.Field()
    # 违法期间法人代表等
    refereesInBreakLaws = scrapy.Field()
    # 负有直接责任的财务人员姓名等
    directInBreakLaws = scrapy.Field()
    # 实际负责人姓名等
    realInBreakLaws = scrapy.Field()   
    # 负有直接责任的中介机构信息
    agencyInBreakLaws = scrapy.Field()
    # 案件性质
    lawCase = scrapy.Field()  
    # 处罚情况
    punish = scrapy.Field() 