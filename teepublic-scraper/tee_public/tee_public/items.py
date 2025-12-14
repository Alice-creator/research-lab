# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    primary_tag = scrapy.Field()
    product_url = scrapy.Field()
    price = scrapy.Field()
    product_image_path = scrapy.Field()
    artist_applied_tags = scrapy.Field()
    trending_tags = scrapy.Field()
    popular_page = scrapy.Field()
    popular_position = scrapy.Field()
