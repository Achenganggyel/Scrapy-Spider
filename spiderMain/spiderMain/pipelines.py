# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

class SpidermainPipeline:
    pass
    # def __init__(self) -> None:
    #     # 新增不同地点的分类
    #     self.file = open('./res/results.json','w+',encoding='utf-8')
    # def file_path(self, request, response=None, info=None):
    #     pass
    # def process_item(self, item, spider):
    #     # 将item转为字典
    #     item_dict = dict(item)
    #     # 将字典以JSON格式写入文件
    #     line = json.dumps(item_dict, ensure_ascii=False) + "\n"
    #     self.file.write(line)
    #     return item
    # def close_spider(self, spider):
    #     # 关闭文件
    #     self.file.close()