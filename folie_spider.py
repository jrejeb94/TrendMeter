import scrapy
from scrapy import Spider, Request

class FolieSpider(scrapy.Spider):
    name = 'folie'
    start_urls = [
        'https://www.foliecosmetic.com/3-parfums-pas-cher-parfum-discount',
        'https://www.foliecosmetic.com/5-maquillage-pas-cher-cosmetique-a-prix-discount',
        'https://www.foliecosmetic.com/368-cheveux',
        'https://www.foliecosmetic.com/8-soins'
    ]
    def parse (self,response):
        for url in response.css('.product_img_link::attr(href)').getall():
            yield Request(url, callback=self.parse_product, meta={'url':url.split("/")[3]})

        url_next_page=response.css('#pagination_next_bottom a::attr(href)').get()

        if url_next_page:
            yield Request(response.urljoin(url_next_page), callback=self.parse)

    def parse_product (self, response):
        #S'il n'y a pas de commentaire, on ne récupère rien
        if not response.css('.netreviews_note_generale::text').get():
            return
        retailer_id="foliecosmetic_com"
        yield{
            ###Table Product
            # 'product_id':response.css('#product_reference span::attr(content)').get(),
            # 'client_id':response.css('.breadcrumb-product::text').get().split("-")[0].strip(),
            # 'product_name':response.css('.breadcrumb-product::text').get().split("-")[1].strip(),
            # 'price':response.css('#our_price_display::attr(content)').get(),
            # 'avg_mark':response.css('.netreviews_note_generale::text').get().strip(),
            # 'product_type': response.meta['url'],
            # 'retailer_id':retailer_id

            
            ###Table Client
            'client_id':response.css('.breadcrumb-product::text').get().split("-")[0].strip(),
            'retailer_id':retailer_id,
            'product_id':response.css('#product_reference span::attr(content)').get(),
            'product_type':response.meta['url']

        }
        
        # product_infos={
        #     'product_brand':response.css('.breadcrumb-product::text').get().split("-")[0].strip(),
        #     'product_name':response.css('.breadcrumb-product::text').get().split("-")[1].strip(),
        #     'product_price':response.css('#our_price_display::attr(content)').get(),
        #     'product_id':response.css('#product_reference span::attr(content)').get(),
        #     'product_avg_mark':response.css('.netreviews_note_generale::text').get().strip(), 
        # }

        # for review in response.css('.netreviews_review_part'):
        #     [comment_usefull, comment_useless] = review.css('.netreviews_helpful_block .netreviewsVote span::text').getall()
        #     yield {
        #         #**product_infos,

        #         ### Table review
        #         'retailer_id':retailer_id,
        #         'product_id':response.css('#product_reference span::attr(content)').get(),
        #         'author_id': review.css('.netreviews_customer_name::text').get().strip(),
        #         'mark':review.css('.netreviews_reviews_rate::text').get().strip()[0],
        #         'review_date':review.css('.netreviews_customer_name span::text').get().split(" ")[-1],
        #         'review_title':None,
        #         'review_txt':review.css('.netreviews_customer_review::text').get(),
        #         'useful_review': comment_usefull,
        #         'useless_review': comment_useless
        #     }