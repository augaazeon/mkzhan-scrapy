# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from mkzhan.items import beforeTheFallItem

class BeforethefallSpider(Spider):
    name = 'beforeTheFall'
    # allowed_domains = ['']
    start_urls = ['https://www.mkzhan.com/211879/']

    def parse(self, response):
        for chapter_url in response.xpath('//li[contains(@class,"chapter__item")]//a/@data-hreflink').extract():
            url = response.url + chapter_url.split('/')[-1]
            yield Request(url,callback=self.parse_chapter)


    def parse_chapter(self,response):
        item = beforeTheFallItem()
        chapter_title = response.xpath('//title/text()').extract_first().split(' ')[1]
        url_item = response.xpath('//img/@data-src').extract()
        # for page_num,url in enumerate(url_item):
        item['image_urls'] = url_item
        # item['page_num'] = page_num
        item['chapter_title'] = chapter_title
        yield item
