import scrapy
from scrapy import Spider, Request
import urllib
import json
import datetime

class MarionnaudSpider(scrapy.Spider):
    name = 'marionnaud'
    start_urls = [
        'https://www.marionnaud.fr/maquillage/teint/c/M0100?pageSize=100',
        'https://www.marionnaud.fr/maquillage/yeux/c/M0200?pageSize=100',
        'https://www.marionnaud.fr/maquillage/levres/c/M0300?pageSize=100',
        'https://www.marionnaud.fr/maquillage/ongles/c/M0400?pageSize=100',
    ]

    def parse(self,response):
        for product_page_link in response.css('.page-link::attr(href)').getall():
            other_page_url = urllib.parse.urljoin(response.url, product_page_link.strip()) + "&pageSize=20"
            yield Request(other_page_url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        base_url='https://www.marionnaud.fr'

        for product_link in response.css('.productMainLink > a::attr(href)').getall():
            yield Request(base_url+product_link, callback=self.parse_product)


    def parse_product(self, response):
        # Récupérer l'URL de l'API des reviews
        product_id=response.url.split("/")[-1][3:]
        base_url= "/".join(response.url.split("/")[:-1])
        url_review= base_url+ '/' + product_id + '/reviews/0/6'
        product_type=response.url.split("/")[5]
        retailer_id='marionnaud_fr',
        retailer_name=response.url.split("/")[2].split(".")[1],
        # yield Request(url_review, callback=self.parse_reviews, meta={
        #     'retailer_id':retailer_id,
        #     'product_id':product_id,
        #     'brand':response.css('.productBrandName::text').get().strip(),
        #     'product_name': response.css('.productName::text').get().strip(),
        #     'avg_mark': response.css('.numberRating::text').get().strip(),
        #     'price':response.css('.finalPrice::text').get().strip(),
        #     'product_type':product_type,
        #     'retailer_name':retailer_name
            
        # })
        
        yield{

                ## Table Client
                # 'client_id':response.css('.productBrandName::text').get().strip(),
                # 'retailer_id':retailer_id,
                # 'product_id':product_id,
                # 'product_type':product_type,

                ## Table product
                # 'product_id':product_id,
                # 'client_id':response.css('.productBrandName::text').get().strip(),
                # 'product_name':response.css('.productName::text').get().strip(),
                # 'price':response.css('.finalPrice::text').get().strip(),
                # 'avg_mark':response.css('.numberRating::text').get().strip(),
                # 'product_type':product_type,
                # 'retailer_id':retailer_id,

                ##Table Retailer
                'retailer_id':retailer_id,
                'retailer_name': retailer_name
        }

    def parse_reviews(self, response):
        reviews = json.loads(response.text)
        i=0
        for review in reviews:
            i+=1
            timestamp=review['date']/1000
            formated_date  = datetime.datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d")
            yield {

                # ## Table product
                # 'product_id':response.meta['product_id'],
                # 'client_id':response.meta['brand'],
                # 'product_name':response.meta['product_name'],
                # 'price':response.meta['price'],
                # 'avg_mark':response.meta['avg_mark'],
                # 'product_type':response.meta['product_type'],
                # 'retailer_id':response.meta['retailer_id'],
                

                ##Table Retailer
                #'retailer_id':response.meta['retailer_id'],
                #'retailer_name': response.meta['retailer_name']

                ## Table review
                #'retailer_id':response.meta['retailer_id'],
                #'product_id':response.meta['product_id'],
                #'author_id':review['alias'].strip(),
                #'mark': review['rating'],
                #'review_date':formated_date,
                #'review_title':review['headline'],
                #'review_txt':review['comment'],
                #'useful_review':None,
                #'useless_review':None,

                ## Table client
                #'client_id':response.meta['brand'],
                #'retailer_id':response.meta['retailer_id'],
                #'product_id':response.meta['product_id'],
                #'product_type':response.meta['product_type']
                
                

            }

