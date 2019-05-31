# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class beforeTheFallItem(Item):
    chapter_title = Field()
    image_urls = Field()
    page_num = Field()
    image_paths = Field()