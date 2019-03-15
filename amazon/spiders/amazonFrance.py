# -*- coding: utf-8 -*-
import scrapy
import re 
from amazon.items import AmazonItem, ProductItem, ReviewItem, ConsumerItem
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
        for product in product_page:
            print(product[0])
        print(len(product_page))
        for product in product_page:
            link = product[1]
            name = product[0]
            yield scrapy.Request(link, callback = self.parse_product, meta = {'product_link' : link, 'product_name' : name})
            sleep(1)

    
    def parse_product(self, response):
        
        p = ProductItem()

        # Get the Amazon ID (ASIN) from the url
        try:
            p['product_id'] = re.search("/dp/(.*?)$", response.meta['product_link']).group(1)
        except:
            p['product_id'] = None

        print("product id: ", p['product_id'])

        # Set client id
        p['client_id'] = "LOrealParis"

        # Get the product name
        try:
            name = response.meta['product_name']
        except:
            name = None
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
            if re.search("&Atilde;", name) != None:
                name = re.sub("&Atilde;", "é", name)
            if re.search("&rsquo;", name) != None:
                name = re.sub("&rsquo;", "'", name)

        p['product_name'] = name
        print("name: ", p['product_name'])

        # Get the price
        try:
            price = response.css("#priceblock_ourprice::text").get()
            price = re.search("\d+.\d\d$", price).group()
        except:
            price = None 

        p['price'] = price 

        # Get the average mark
        try:
            avg_mark = response.css("#acrPopover::attr(title)").get()
            avg_mark = re.search("^(\d.\d) étoiles sur 5", avg_mark).group(1)
        except:
            avg_mark = None
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

        # If reviews exist for this product
        if avg_mark is not None:
            yield scrapy.Request(review_link, callback = self.parse_review, meta = {'product': p})

        # yield item

    def parse_review(self, response):


        r = ReviewItem()
        p = response.meta['product']
        print(p)

        review_list = re.findall('<div id="customer_review-(.*?)" class="', response.text)

        for review in review_list:
            review_css = "#customer_review-" + review
            r['retailer_id'] = "amazon_fr"
            r['product_id'] = p['product_id']

            # # Get displayed username
            # try:
            #     author = response.css(review_css + " > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)::text").get()
            # except:
            #     try:
            #         author = response.css(review_css + " > div.genome-widget-row > div.profile-widget-with-avatar > div:nth-child(1) > a.a-profile > div.a-profile-content > span.a-profile-name") 
            #     except:
            #         author = ""
            
            # # Get the user ID from their profile link          
            # try:
            #     profile = response.css(review_css + " > div:nth-child(1) > a.a-profile::attr(href)").get()
            #     profile = re.search("amzn1.account.([A-Z0-9]+)$", profile).group(1)
            #     author += ": " + profile
            # except:
            #     author = None
            #     print("Couldn't find profile link, review id: ", review)
            

            # Regular user
            try:
                author = response.css(review_css + " > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > span:nth-child(1)::text").get()
                profile = response.css(review_css + " > div:nth-child(1) > a.a-profile::attr(href)").get()
                profile = re.search("amzn1.account.([A-Z0-9]+)$", profile).group(1)
                author += ": " + profile
            except:
                # Special user
                try:
                    author = response.css(review_css + " > div.genome-widget-row > div.profile-widget-with-avatar > div:nth-child(1) > a.a-profile > div.a-profile-content > span.a-profile-name::text").get()
                    profile = response.css(review_css + " > div.genome-widget-row > div.profile-widget-with-avatar > div:nth-child(1) > a.a-profile::attr(href)").get()
                    profile = re.search("amzn1.account.([A-Z0-9]+)$", profile).group(1)
                    author += ": " + profile
                except:
                    author = None
            
            r['author_id'] = author 

            mark = response.css(review_css + " > div.a-row > a.a-link-normal::attr(title)").get()
            mark = re.search("^(\d.\d) sur", mark).group(1)
            # replacing to period
            mark = re.sub(r",", ".", mark)
            r['mark'] = mark

            r['review_date'] = response.css(review_css + " > span:nth-child(3)::text").get()
            r['review_title'] = response.css(review_css + " > div.a-row > a:nth-child(3) > span:nth-child(1)::text").get()
            r['review_txt'] = response.css(review_css + " > div:nth-child(5) > span[data-hook = review-body] > span:nth-child(1)::text").get()
            useful = response.css(review_css + " > div:nth-child(6) > div[data-a-expander-name = review_comment_expander] > span.cr-vote > div:nth-child(1) > span[data-hook = helpful-vote-statement]::text").get()
            print(useful)
            if useful != None:
                useful = re.search("^(.*?) personne", useful).group(1)
                if useful == "Une":
                    useful = 1
            else:
                useful = 0
            r['useful_review'] = int(useful)
            r['useless_review'] = None
            
            c = ConsumerItem()

            c['author_id'] = r['author_id']
            c['gender'] = c['eye_color'] = c['hair_color'] = c['skin_concerns'] = c['skintone'] = c['skintype'] = None

            item = AmazonItem()
            item['review'] = r
            item['product'] = p
            item['consumer'] = c

            sleep(2)

            yield item 

        next_review_page = response.css(".a-last > a:nth-child(1)::attr(href)").get()
        if next_review_page is not None:
            if next_review_page[0] == "/":
                next_review_page = "https://www.amazon.fr" + next_review_page
            yield scrapy.Request(next_review_page, callback = self.parse_review, meta = {'product': p})
            
        
