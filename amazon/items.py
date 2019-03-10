# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field()
    #client_id = scrapy.Field()
    product_name = scrapy.Field()
    #price = scrapy.Field()
    #avg_mark = scrapy.Field()
    product_type = scrapy.Field()
    #retailer_id = scrapy.Field()

class ReviewItem(scrapy.Item):
    retailer_id = scrapy.Field()
    product_id = scrapy.Field()
    author_id = scrapy.Field()
    mark = scrapy.Field()
    review_date = scrapy.Field()
    review_title = scrapy.Field()
    review_txt = scrapy.Field()
    useful_review = scrapy.Field()
    useless_review = scrapy.Field()

class ConsumerItem(scrapy.Item):
    author_id = scrapy.Field()
    gender = scrapy.Field()
    eye_color = scrapy.Field()
    hair_color = scrapy.Field()
    skin_concerns = scrapy.Field()
    skintone = scrapy.Field()
    skintype = scrapy.Field()

class AmazonItem(scrapy.Item):
    product = scrapy.Field()
    #review = scrapy.Field()
    #consumer = scrapy.Field()

