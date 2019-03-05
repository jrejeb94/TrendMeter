# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import scrapy

class ProductItem(scrapy.Item):
    product_id = scrapy.Field()
    client_id = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    avg_mark = scrapy.Field()
    product_type = scrapy.Field()
    retailer_id = scrapy.Field()

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

class Date(object):
    def __init__(self):
        self.year = 1988
        self.month = 1
        self.day = 1

    def __init__(self, year, month, day):
        self.setDate(year, month, day)

    def __init__(self, date_str):
        self.setDate(date_str)

    def setDate(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def setDate(self, date_str):
        "Format '2019-02-10T11:44:33.000+00:00' utilisé par Sephora"
        self.year = int(date_str[:4])
        self.month = int(date_str[5:7])
        self.day = int(date_str[8:10])

    def __str__(self):
        result = str(self.day) + " "
        result += ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                   "Juillet", "Août", "Septembre", "Octobre", "Novembre",
                   "Décembre"][self.month-1]
        result += " " + str(self.year)
        return result

class SephoraItem(scrapy.Item):
    product = scrapy.Field()
    review = scrapy.Field()
    consumer = scrapy.Field()

# class SephoraItem(scrapy.Item):
#     # define the fields for your item here like:
#     p_name = scrapy.Field()
#     p_id = scrapy.Field()
#     link = scrapy.Field()
#     brand_name = scrapy.Field()
#     review_count = scrapy.Field()
#     avg_rating = scrapy.Field()
#     rating_count = scrapy.Field()
#     # p_category = scrapy.Field()
#     # p_price = scrapy.Field()
#     reviewer = scrapy.Field()
#     r_star = scrapy.Field()
#     r_eyecolor = scrapy.Field()
#     r_skintype = scrapy.Field()
#     r_title = scrapy.Field()
#     r_review = scrapy.Field()
