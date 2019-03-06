import scrapy
from scrapy import Spider, Request

class FolieSpider(scrapy.Spider):
    name = 'loreal'
    start_urls = [
        'https://www.loreal-paris.fr/maquillage',
        'https://www.loreal-paris.fr/soin-de-la-peau',
        'https://www.loreal-paris.fr/coloration',
        'https://www.loreal-paris.fr/cheveux',
        'https://www.loreal-paris.fr/homme'
    ]

    def parse(self, response):
         for url in response.css('.df-product-list-box >a::attr(href)').getall():
             yield Request(response.urljoin(url), callback=self.parse_product)

    def parse_product(self, response):
        brand="Loreal-Paris"
        retailer_id="loreal-paris_fr"
        
        yield{

        ### Table product
        #     'product_id':response.css('.product-page-holder.js-product-wrapper::attr(data-product)').get().strip(),
        #     'client_id':brand,
        #     'product_name':response.css('.product-name .js-product-name::text').get().strip(),
        #     'price':response.css('.df-product-price-info div[itemprop="price"]::text').get().strip(),
        #     'avg_mark':response.css('#bvseo-aggregateRatingSection .bvseo-ratingValue::text').get().strip(),
        #     'product_type':response.css('.product-name .product-category::text').get().strip(),
        #     'retailer_id':retailer_id

        ###Table Client 
             'client_id':brand,
             'retailer_id':retailer_id,
             'product_id':response.css('.product-page-holder.js-product-wrapper::attr(data-product)').get().strip(),
             'product_type':response.css('.product-name .product-category::text').get().strip(),

             }

        # product_infos={
        #     'product_name':response.css('.product-name .js-product-name::text').get().strip(),
        #     'product_id':response.css('.product-page-holder.js-product-wrapper::attr(data-product)').get().strip(),
        #     'product_category':response.css('.product-name .product-category::text').get().strip(),
        #     'product_price':response.css('.df-product-price-info div[itemprop="price"]::text').get().strip(),
        #     'product_avg_mark':response.css('#bvseo-aggregateRatingSection .bvseo-ratingValue::text').get().strip(),
        #     'product_nb_reviews':response.css('#bvseo-aggregateRatingSection .bvseo-reviewCount::text').get().strip()
        #     }
        for review in response.css('.bvseo-review'):
            date=review.css('.bvseo-pubdate::text').get().split(" ")[-1]
            date="{0}/{1}/{2}".format(*date.split("-"))
            # yield {
            #     #**product_infos,
            #     'retailer_id':retailer_id,
            #     'product_id':response.css('.product-page-holder.js-product-wrapper::attr(data-product)').get().strip(),
            #     'author_id': review.css('span[itemprop="author"]::text').get().strip(),
            #     'mark':review.css('span [itemprop="ratingValue"]::text').get().strip(),
            #     'review_date':date,
            #     'review_title':(review.css('span[itemprop="name"]::text').get() or '').strip(),
            #     'review_txt':review.css('span[itemprop="description"]::text').get().strip(),
            #     'useful_review': None,
            #     'useless_review': None
            # }
        url_next_page=response.css('.bvseo-paginationLink::attr(href)').get()
        if url_next_page:
            yield Request(url_next_page, callback=self.parse)



    # def parse (self,response):
    #     for url in response.css('.product_img_link::attr(href)').getall():
    #         yield Request(url, callback=self.parse_product)

    #     url_next_page=response.css('#pagination_next_bottom a::attr(href)').get()

    #     if url_next_page:
    #         yield Request(response.urljoin(url_next_page), callback=self.parse)

    # def parse_product (self, response):
    #     #S'il n'y a pas de commentaire, on ne récupère rien
    #     if not response.css('.netreviews_note_generale::text').get():
    #         return

    #     product_infos={
    #         'product_brand':response.css('.breadcrumb-product::text').get().split("-")[0].strip(),
    #         'product_name':response.css('.breadcrumb-product::text').get().split("-")[1].strip(),
    #         'product_price':response.css('#our_price_display::attr(content)').get(),
    #         'product_id':response.css('#product_reference span::attr(content)').get(),
    #         'product_avg_mark':response.css('.netreviews_note_generale::text').get().strip(), 
    #     }

    #     for review in response.css('.netreviews_review_part'):
    #         [comment_usefull, comment_useless] = review.css('.netreviews_helpful_block .netreviewsVote span::text').getall()
    #         yield {
    #             **product_infos,
    #             'author': review.css('.netreviews_customer_name::text').get().strip(),
    #             'comment_date':review.css('.netreviews_customer_name span::text').get().split(" ")[-1],
    #             'mark':review.css('.netreviews_reviews_rate::text').get().strip()[0],
    #             'comment':review.css('.netreviews_customer_review::text').get(),
    #             'comment_usefull': comment_usefull,
    #             'comment_useless': comment_useless
    #         }