# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
            # referer=item['url']
            for page_num,image_url in enumerate(item['image_urls']):
                yield Request(image_url,meta={'item': item,'page_num':page_num})#传参item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # image_url = request.url
        page_num = request.meta['page_num']
        folder = item['chapter_title']#设置文件夹名
        folder_strip = folder.strip()
        # image_guid = image_url.split('/')[-1].split('!')[0]
        image_guid = page_num

        file_name = u'{0}/{1}.{2}'.format(folder_strip, image_guid,'jpg')#路径
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_paths
        return item
