# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommerceItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    model = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    reviews = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
