# -*- coding: utf-8 -*-
import scrapy

class EcommerceSpider(scrapy.Spider):
    def __init__(self, url=None, *args, **kwargs):
        if url is not None:
            self.start_urls = [url]
        else:
            self.start_urls = []
        super(EcommerceSpider, self).__init__(*args, **kwargs)
