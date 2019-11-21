# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class WbimgsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['imglink'])

    def item_completed(self, results, item, info):
        # print(results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['imgpath'] = image_paths
        return item
