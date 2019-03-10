# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter

class ValidateItemPipeline(object):

    def process_item(self, item, spider):
        if not all(item.values()):
            print ('MISSING VALUES')
            return item
        else:
            return item

class WriteItemPipeline(object):

    def __init__(self):
        self.filename_p = 'amazon_product.csv'
        self.filename_r = 'amazon_review.csv'
        self.filename_c = 'amazon_consumer.csv'

    def open_spider(self, spider):
        self.csvfile_p = open(self.filename_p, 'wb')
        self.exporter_p = CsvItemExporter(self.csvfile_p)
        self.exporter_p.start_exporting()

        # self.csvfile_r = open(self.filename_r, 'wb')
        # self.exporter_r = CsvItemExporter(self.csvfile_r)
        # self.exporter_r.start_exporting()

        # self.csvfile_c = open(self.filename_c, 'wb')
        # self.exporter_c = CsvItemExporter(self.csvfile_c)
        # self.exporter_c.start_exporting()

    def close_spider(self, spider):
        self.exporter_p.finish_exporting()
        self.csvfile_p.close()
        
        # self.exporter_c.finish_exporting()
        # self.csvfile_c.close()

        # self.exporter_r.finish_exporting()
        # self.csvfile_r.close()

       

    def process_item(self, item, spider):
        self.exporter_p.export_item(item['product'])
        #self.exporter_r.export_item(item['review'])
        #self.exporter_c.export_item(item['consumer'])
        # return item

# class AmazonPipeline(object):
#     def process_item(self, item, spider):
#         return item
