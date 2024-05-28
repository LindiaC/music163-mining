# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exporters import CsvItemExporter
 
class WyymusicPipeline:
    def __init__(self):
        self.MusicListFile = open("MusicList.csv", "wb+")   #保存为csv格式
        self.MusicListExporter = CsvItemExporter(self.MusicListFile, encoding='utf8')
        self.MusicListExporter.start_exporting()
 
    def process_item(self, item, spider):
        if spider.name == 'MusicList':
            self.MusicListExporter.export_item(item)
            return item