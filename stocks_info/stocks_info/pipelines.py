# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# class StocksInfoPipeline:
#     def process_item(self, item, spider):
#         return item

from colorlog import ColoredFormatter
import logging

class StocksInfoPipeline:
    # def __init__(self):
    #     self.logger = logging.getLogger('scrapy')
    #     handler = logging.StreamHandler()
    #     formatter = ColoredFormatter('%(log_color)s%(levelname)-8s%(reset)s %(message)s')
    #     handler.setFormatter(formatter)
    #     self.logger.addHandler(handler)
    #     self.logger.setLevel(logging.DEBUG)
    #
    # def process_item(self, item, spider):
    #     # 用不同的颜色输出日志
    #     self.logger.debug(f"Processing item: {item}")
    #     return item

    def process_item(self, item, spider):
        print(item)
        return item
