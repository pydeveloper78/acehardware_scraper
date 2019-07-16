# -*- coding: utf-8 -*-
import scrapy
from ecommerce.spiders import EcommerceSpider
from ecommerce.items import EcommerceItem

from bs4 import BeautifulSoup
import json
import requests

class AcehardwareSpider(EcommerceSpider):
    name = 'acehardware'
    allowed_domains = ['www.acehardware.com']
    
    def parse(self, response):
        if 'isProduct' in response.meta and response.meta['isProduct']:
            soup = BeautifulSoup(response.body, 'lxml')
            productJson = json.loads(soup.find('script', attrs={'id':'data-mz-preload-product'}).encode_contents())

            hdrs = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Authorization': '516a63a6-9f21-4dbe-b9f4-edc4b7387ea7'
            }
            res = requests.get('https://readservices-b2c.powerreviews.com/m/4403/l/en_US/product/%s/reviews?' % str(productJson["productCode"]), headers=hdrs)
            parsed = json.loads(res.text)

            item = EcommerceItem()
            
            item['id'] = productJson["productCode"]
            item['name'] = productJson["content"]["productName"]
            item['model'] = productJson["mfgPartNumber"].strip()
            item['url'] = response.url
            item['brand'] = ""
            for p in productJson["properties"]:
                if p["attributeDetail"]["name"] == 'Brand Name':
                    item['brand'] = p["values"][0]["stringValue"]
            try:
                item['reviews'] = parsed["results"][0]["rollup"]["average_rating"]
            except:
                item['reviews'] = 0
            try:
                item['rating'] = parsed["results"][0]["rollup"]["review_count"]
            except:
                item['rating'] = 0
            
            if productJson["price"]["onSale"]:
                item['price'] = productJson["price"]["salePrice"]
            else:
                item['price'] = productJson["price"]["price"]
            
            yield item
        
        else:
            for u in response.xpath('//li[contains(@class, "mz-productlist-item")]//a[@class="mz-productlisting-title"]/@href').extract():
                yield scrapy.Request(u, meta={'isProduct': True})
            
            next_page = response.xpath('//a[@class="mz-pagenumbers-next"]/@href').extract_first()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), meta={'isProduct': False})