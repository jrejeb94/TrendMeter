from scrapy import Spider, Request
from sephora.items import *
import re
import pandas as pd
import json
import math
import time

n_count_tot = 0

class SephoraSpider(Spider):

	name = "sephora_spider"
	allowed_urls = ["https://www.sephora.fr", "https://api.bazaarvoice.com"]
	start_urls = ["https://www.sephora.fr"]

	#parse all products on Sephora via the BazaarVoice API

	def parse(self, response):
		#parse json with all products 100 by 100, which is the maximal limit
		url = 'https://api.bazaarvoice.com/data/products.json?passkey=iohrnzjadededr160osgfvimy&apiversion=5.5&displaycode=3232-fr_fr&limit=100&offset='

		for i in range(0,24500,100):
			yield Request(url+str(i), callback=self.parse_products)


	def parse_products(self, response):
		#parse the 100 given product by the API
		products = json.loads(response.text)['Results']

		for product in products:
			if product['Active']:	#if the product is active, we go to the url to get the price
				yield Request(product['ProductPageUrl'], callback=self.parse_detail_seph, meta={'p_id':product['Id']})


	def parse_detail_seph(self, response):
		p_id = response.meta['p_id']

		begin = "<span class='price-sales price-sales-standard'>\n<span>"
		end = "&#8364;</span>" # &#8364; is €
		list_prices = re.findall(begin + ".*?" + end, response.text)
		if (len(list_prices) == 0):
			print("ERROR: no prices found!")
			file = open("log.txt", 'w')
			file.write(response.text)
			file.close()
			return -1

		price = list_prices[0][len(begin):-len(end)]
		print(p_id + " at " + price)

		url = 'https://api.bazaarvoice.com/data/products.json?passkey=iohrnzjadededr160osgfvimy&apiversion=5.5&displaycode=3232-fr_fr&filter=id:eq:'+p_id+'&stats=reviews'

		yield Request(url, callback=self.parse_detail_BV, meta={'p_id':p_id, "price":price})


	def parse_detail_BV(self, response):
		p_id = response.meta['p_id']
		price = response.meta['price']

		data = json.loads(response.text)['Results']

		if (len(data) == 0):
			print("No result for product number: " + p_id)
			file = open("log.txt", 'w')
			file.write(response.text)
			file.close()
			return -1

		data = data[0]

		name = data['Name']
		link = data['ProductPageUrl']
		brand_name = data['Brand']['Name']
		review_count = data['ReviewStatistics']['TotalReviewCount']
		try:
			category = data['CategoryId']
		except:
			category = None
		try:
			rating = data['ReviewStatistics']['AverageOverallRating']
		except:
			rating = None
		try:
			#rating_count = data['ReviewStatistics']['RatingDistribution'][0]['Count']
			rating_count = data['ReviewStatistics']['TotalReviewCount']
		except:
			rating_count = 0

		p_item = ProductItem()
		p_item['product_id'] = p_id
		p_item['client_id'] = brand_name
		p_item['product_name'] = name
		p_item['price'] = price
		p_item['avg_mark'] = rating
		p_item['product_type'] = category[:category.find("_")]
		p_item['retailer_id'] = "sephora_fr"

		links3 = ['https://api.bazaarvoice.com/data/reviews.json?apiversion=5.5&passkey=iohrnzjadededr160osgfvimy'+
				  '&filter=productid:eq:'+
		 		  p_id + '&sort=submissiontime:desc&include=authors,products,comments&limit=100']

		for url in links3:
			yield Request(url, callback=self.parse_reviews,
		 		  meta={'p_id':p_id, 'name':name, 'link':link, 'brand_name':brand_name,
				  		'review_count':review_count, 'rating':rating, 'rating_count':rating_count,
						'product':p_item, 'offset':0})


	def parse_reviews(self, response):

		p_id = response.meta['p_id']
		name = response.meta['name']
		link = response.meta['link']
		brand_name = response.meta['brand_name']
		review_count = response.meta['review_count']
		rating = response.meta['rating']
		rating_count = response.meta['rating_count']
		p_item = response.meta['product']
		offset = response.meta['offset']

		data = json.loads(response.text)
		reviews = data['Results']

		#create code here which arranges the data from the json dictionary into a dataframe

		n_count = 0
		global n_count_tot

		for review in reviews:
			try:
				r_id = review['Id']
			except:
				r_id  = "R" + str(n_count_tot)

			try:
				reviewer = review['UserNickname']
			except:
				reviewer = "C" + str(n_count_tot)
			if type(reviewer) != str:
				reviewer = "C" + str(n_count_tot)

			try:
				r_date = Date(review['SubmissionTime'])
			except:
				r_date = None
			try:
				r_star = review['Rating']
			except:
				r_star = None

			try:
				r_gender = review['ContextDataValues']['Gender']['Value']
			except:
				r_gender = None

			try:
				r_eyecolor = review['ContextDataValues']['Eyes']['Value']
			except:
				r_eyecolor = None

			try:
				r_skintype = review['ContextDataValues']['Skin']['Value']
			except:
				r_skintype = None

			try:
				r_title = review['Title']
			except:
				r_title = None

			try:
				r_review = review['ReviewText']
			except:
				r_review = None

			try:
				r_useful = review['TotalPositiveFeedbackCount']
			except:
				r_useful = None
			try:
				r_useless = review['TotalNegativeFeedbackCount']
			except:
				r_useless = None

			#need to create an error handler for empty data for reviews

			print ('BRAND: {} ; PRODUCT: {}'.format(brand_name, name))

			c_item = ConsumerItem()
			c_item['author_id'] = "S_" + reviewer
			c_item['gender'] = r_gender
			c_item['eye_color'] = r_eyecolor
			c_item['hair_color'] = None
			c_item['skin_concerns'] = None
			c_item['skintone'] = None
			c_item['skintype'] = r_skintype

			r_item = ReviewItem()
			r_item['retailer_id'] = "sephora_fr"
			r_item['product_id'] = p_id
			r_item['author_id'] = "S_" + reviewer
			r_item['mark'] = r_star
			r_item['review_date'] = str(r_date)
			r_item['review_title'] = r_title
			r_item['review_txt'] = r_review
			r_item['useful_review'] = r_useful
			r_item['useless_review'] = r_useless

			item = SephoraItem()
			item['product'] = p_item
			item['review'] = r_item
			item['consumer'] = c_item

			n_count += 1
			n_count_tot += 1

			yield item

		print ('ACTUAL NUMBER PULLED {}'.format(n_count))
		print ('TOTAL NUMBER PULLED {}'.format(n_count_tot))

		if n_count == 100:
			offset += 100
			links3 = ['https://api.bazaarvoice.com/data/reviews.json?apiversion=5.5&passkey=iohrnzjadededr160osgfvimy'+
					  '&filter=productid:eq:'+
			 		  p_id + '&sort=submissiontime:desc&include=authors,products,comments&limit=100&offset=' + str(offset)]

			for url in links3:
				yield Request(url, callback=self.parse_reviews,
			 		  meta={'p_id':p_id, 'name':name, 'link':link, 'brand_name':brand_name,
					  		'review_count':review_count, 'rating':rating, 'rating_count':rating_count,
							'product':p_item, 'offset':offset})
