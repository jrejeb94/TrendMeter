# -*- coding: utf-8 -*-
import scrapy
import re 
from amazon.items import AmazonItem, ProductItem
from time import sleep 

class AmazonfranceSpider(scrapy.Spider):
    name = 'amazonFrance'
    allowed_domains = ['amazon.fr']
    proxies = {
        "https_proxy" : "118.174.220.231",
        "http_proxy" : "182.253.152.109"
    }
    start_urls = ['https://www.amazon.fr/s?ie=UTF8&field-keywords=l%27or%C3%A9al']


    def parse(self, response):
        
        begin = 'a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" title='
        
        # Searching within the html response because CSS selector of the product links are not all the same
        # Find all the occurrences of product names and links to their pages in the html response
        product_page = re.findall(begin + '\"(.*?)\" href=\"(.*?)\">', response.text)
        
        for product in product_page[:3]:
            link = product[1]
            name = product[0]
            yield scrapy.Request(link, callback = self.parse_product, meta = {'product_link' : link, 'product_name' : name})
            sleep(2)

    
    def parse_product(self, response):
        
        p = ProductItem()

        # Get the Amazon ID (ASIN) from the url
        p['product_id'] = re.search("/dp/(.*?)$", response.meta['product_link']).group(1)
        print("product id: ", p['product_id'])

        # Set client id
        p['client_id'] = "LOrealParis"

        # Get the product name
        name = response.meta['product_name']
        # Replace html special charcters as the semicolon might be confusing for csv format
        if re.search("&(\w+);", name) != None:
            print("special character found")
            if re.search("&eacute;", name) != None:
                name = re.sub("&eacute;", "é", name)
            if re.search("&egrave;", name) != None:
                name = re.sub("&egrave;", "è", name)
            if re.search("&euml;", name) != None:
                name = re.sub("&euml;", "ë", name)
            if re.search("&ecirc;", name) != None:
                name = re.sub("&ecirc;", "ê", name)
            if re.search("&acirc;", name) != None:
                name = re.sub("&acirc;", "â", name)
            if re.search("&agrave;", name) != None:
                name = re.sub("&agrave;", "à", name)
            if re.search("&icirc;", name) != None:
                name = re.sub("&icirc;", "î", name)
            if re.search("&iuml;", name) != None:
                name = re.sub("&iuml;", "ï", name)
            if re.search("&ocirc;", name) != None:
                name = re.sub("&ocirc;", "ô", name)
            if re.search("&ugrave;", name) != None:
                name = re.sub("&ugrave;", "ù", name)

        p['product_name'] = name
        print("name: ", p['product_name'])

        # Get the price
        price = response.css("#priceblock_ourprice::text").get()
        price = re.search("\d+.\d\d$", price).group()
        p['price'] = price 

        # Get the average mark
        avg_mark = response.css("#acrPopover::attr(title)").get()
        avg_mark = re.search("^(\d.\d) étoiles sur 5", avg_mark).group(1)
        p['avg_mark'] = avg_mark

        # Get the type of product
        cat_list = response.xpath("//tr[@id='SalesRank']/td[@class='value']/ul/li/span[2]/a").getall() 
        if cat_list == None:
            cat_list = response.xpath("//tr[@id='SalesRank']/td[@class='value']").get()
            p['product_type'] = re.search("\d en (.*?) \(<a href", cat[0]).group(1) 
        else:
            categories = ""
            for cat in cat_list:
                categories += re.search(">(.*?)<",cat).group(1)
                categories += ", "
            
            # Remove the last two characters (", ")
            categories = categories[:-2] 
        p['product_type'] = categories
        print("product type: ", p['product_type'])

        # Set retailer id
        p['retailer_id'] = 'amazon_fr'

        item = AmazonItem()
        item['product'] = p

        yield item

        # item['product_id'] = str(response.css(".item-model-number > td:nth-child(2)::text").get())
        # with open("log_id.txt", 'w+') as f:
        #     f.write(item['product_id'])
        # yield item
               # 'brand' : response.css("div.column:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text").get()
        
        # yield {
        #     'Product' : {
        #         'product_id' : response.css(".item-model-number > td:nth-child(2)::text").get(),
        #         'brand' : response.css("div.column:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text").get(),
        #         'product_name' : response.css("#productTitle::text").get(),
        #         'price' : response.css("#priceblock_ourprice::text").get(),
        #         'avg_mark' : response.css("#a-popover-content-7 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)::text").re(r'[0-5].[0-9]'),
        #         'product_type' : null,
        #         'retailer_id' : "amazon",
        #     }
        # }

        # #follows link to review page
        # review_page = response.css(".a-link-emphasis::attr(href)")[0]
        # response.follow(review_page, callback = self.parse_review)
        # #https://www.amazon.fr/LOr%C3%A9al-Paris-Fluide-Accord-Parfait/dp/B00SXKWB42/
        # #https://www.amazon.fr/LOr%C3%A9al-Paris-Fluide-Accord-Parfait/product-reviews/B00SXKWB42/




    def parse_review(self, response):
        for review in response.css("#cm_cr-review_list::text"):
            yield {
                'Review' : {
                    'author_id' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)::text").get(),
                    'mark' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(2) > a:nth-child(1) > i:nth-child(1) > span:nth-child(1)::text").get(),
                    'review_date' : response.css("#customer_review-RXKTKKZYIVXN9 > span:nth-child(3)::text").get(),
                    'review_title' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(2) > a:nth-child(3)::text").get(),
                    'review_txt' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(5) > span:nth-child(1)::text").get(),
                    'useful_review' : response.css(".comments-for-RXKTKKZYIVXN9 > div:nth-child(1) > span:nth-child(1) > div:nth-child(1) > span:nth-child(1)::text").re(r'^[0-9A-Za-z]+'), #regex for nuber & word at the beginning of the sentence
                    'useless_review' : null,
                }
            }
        
        #follows link to next page
        next_review_page = response.css(".a-last > a:nth-child(1)::attr(href)")[0]
        if next_review_page is not None:
            yield response.follow(next_review_page, callback=self.parse_review)
