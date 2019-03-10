# -*- coding: utf-8 -*-
import scrapy
import re 
from amazon.items import AmazonItem, ProductItem, ReviewItem
from time import sleep 

class AmazonfranceSpider(scrapy.Spider):
    name = 'amazonFrance'
    allowed_domains = ['amazon.fr']
    proxies = {
        "https_proxy" : "118.174.220.231",
        "http_proxy" : "182.253.152.109"
    }
    start_urls = ['https://www.amazon.fr/s?ie=UTF8&field-keywords=l%27or%C3%A9al',\
                  'https://www.amazon.fr/s/page=2&keywords=l%27or%C3%A9al&ie=UTF8',\
                  'https://www.amazon.fr/s/page=3&keywords=l%27or%C3%A9al&ie=UTF8']


    def parse(self, response):
        
        begin = 'a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" title='
        
        # Searching within the html response because CSS selector of the product links are not all the same
        # Find all the occurrences of product names and links to their pages in the html response
        product_page = re.findall(begin + '\"(.*?)\" href=\"(.*?)\">', response.text)
        
        for product in product_page[:1]:
            link = product[1]
            name = product[0]
            yield scrapy.Request(link, callback = self.parse_product, meta = {'product_link' : link, 'product_name' : name})
            sleep(1)

    
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

        # item = AmazonItem()
        # item['product'] = p        

        begin = "https://www.amazon.fr/product-reviews/"
        end = "/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

        review_link = begin + p['product_id'] + end
        yield scrapy.Request(review_link, callback = self.parse_review, meta = {'product': p})

        # yield item

    def parse_review(self, response):


        # for review in response.css("#cm_cr-review_list::text"):
        #     yield {
        #         'Review' : {
        #             'author_id' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)::text").get(),
        #             'mark' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(2) > a:nth-child(1) > i:nth-child(1) > span:nth-child(1)::text").get(),
        #             'review_date' : response.css("#customer_review-RXKTKKZYIVXN9 > span:nth-child(3)::text").get(),
        #             'review_title' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(2) > a:nth-child(3)::text").get(),
        #             'review_txt' : response.css("#customer_review-RXKTKKZYIVXN9 > div:nth-child(5) > span:nth-child(1)::text").get(),
        #             'useful_review' : response.css(".comments-for-RXKTKKZYIVXN9 > div:nth-child(1) > span:nth-child(1) > div:nth-child(1) > span:nth-child(1)::text").re(r'^[0-9A-Za-z]+'), #regex for nuber & word at the beginning of the sentence
        #             'useless_review' : null,
        #         }
        #     }
        
        # #follows link to next page
        # next_review_page = response.css(".a-last > a:nth-child(1)::attr(href)")[0]
        # if next_review_page is not None:
        #     yield response.follow(next_review_page, callback=self.parse_review)
        #/LOréal-Paris-Fluide-Accord-Parfait/product-reviews/B00SXKWB42/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews
        
        #customer_review-RXKTKKZYIVXN9

        r = ReviewItem()
        p = response.meta['product']

        review_list = re.findall('<div id="customer_review-(.*?)" class="', response.text)

        for review in review_list:
            review_css = "#customer_review-" + review
            r['retailer_id'] = "amazon_fr"
            r['product_id'] = p['product_id']
            r['author_id'] = response.css(review_css + " > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)::text").get()
            mark = response.css(review_css + " > div.a-row > a.a-link-normal::attr(title)").get()
            mark = re.search("^(\d.\d) sur", mark).group(1)
            # replacing to period
            mark = re.sub(r",", ".", mark)
            r['mark'] = mark
            r['review_date'] = response.css(review_css + " > span:nth-child(3)::text").get()
            r['review_title'] = response.css(review_css + " > div.a-row > a:nth-child(3) > span:nth-child(1)::text").get()
            r['review_txt'] = response.css(review_css + " > div:nth-child(5) > span:nth-child(1)::text").get()
            useful = response.css(review_css + " > div:nth-child(6) > div[data-a-expander-name = review_comment_expander] > span.cr-vote > div:nth-child(1) > span[data-hook = helpful-vote-statement]::text").get()
            print(useful)
            if useful != None:
                useful = re.search("^(.*?) personne", useful).group(1)
                if useful == "Une":
                    useful = '1'
            r['useful_review'] = useful
            r['useless_review'] = None
            
            item = AmazonItem()
            item['review'] = r
            item['product'] = p

            sleep(1)

            yield item 

        next_review_page = response.css(".a-last > a:nth-child(1)::attr(href)").get()
        if next_review_page is not None:
            yield scrapy.Request(next_review_page, callback = self.parse_review)
        


#customer_review-"RXKTKKZYIVXN9"
#customer_review-R3HXVZANAUV6XC > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)