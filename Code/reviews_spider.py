#!/usr/bin/env python
# coding: utf-8


import scrapy
import logging
import json

class QuotesSpider(scrapy.Spider):
    name = "reviews"
    def start_requests(self):
        urls = ['https://www.g2.com/products/hubspot/reviews.html?focus_review=589034&product_id=hubspot',
                ]
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse)
            
#     custom_settings = {
#         'LOG_LEVEL': logging.WARNING,
#         'ITEM_PIPELINES': {'JsonWriterPipeline': 1}, # Used for pipeline 1
#         'FEED_FORMAT':'json',                                 # Used for pipeline 2
#         'FEED_URI': 'reviewresult.json'     
            
    def parse(self, response):
        page = response.url.split["="][-2]
        filename = 'g2_review-%s.html' % page
        with open (filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        for review in response.css('div[itemprop*=review]'):
            yield {
                'author': response.css('span[itemprop*=author]::text').getall(),
                'company_size' : response.css('span.ml-4th::text').getall(),
                'role' : response.css('div.mt-4th::text').getall(),
                'date' : response.css('time::text').getall(),
                'reviews': {'question' : response.css('h5.l5::text').getall(),
                            'answer' : response.css('p.formatted-text::text').getall()}
                
            }
        

        next_page = response.xpath("//li[contains(., 'Next')]/a/@href").getall()         
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('quoteresult.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
            

