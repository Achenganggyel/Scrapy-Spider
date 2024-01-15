# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
# 支持对不同地点area保存的不同
class SpidermainPipeline(object):
    def __init__(self):
        self.data = {}
        self.path = '../res/'

    def process_item(self, item, spider):
        area = item['area']  # 假设area字段表示省市
        # 如果字典中尚未包含area对应的数据，创建一个新的列表
        if area not in self.data:
            self.data[area] = []
        # 添加item到对应area的列表中
        item_json = json.dumps(dict(item), ensure_ascii=False) # 要将item转换字典
        self.data[area].append(item_json)
        return item

    def close_spider(self, spider):
        for area, data in self.data.items():
            path = self.path + area + '.json'
            with open(path, 'w+', encoding='utf-8') as file:
                 for item in data:
                     file.write(item + '\n')