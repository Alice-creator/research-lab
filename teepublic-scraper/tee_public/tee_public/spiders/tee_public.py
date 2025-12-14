import scrapy 
from dotenv import load_dotenv
import os
from tee_public.spiders.utils import add_or_replace_query_string, get_page_num, extract_next_href
from tee_public.spiders.helpers import tee_public as helper
from tee_public.items import ProductItem

load_dotenv()

class TeepublicSpider(scrapy.Spider):
    name = "tee_public_scraper"
    allowed_domains = [os.getenv("DOMAINS")]
    start_urls = [os.getenv("STARTING_URLS")]

    # Define Storing position
    custom_settings = {
        "FEEDS": {
            "exports/tee_public_result.jsonl": {
                "format": "jsonlines",
                "overwrite": True,
                "encoding": "utf8"
            }
        }
    }

    # Collect website theme and url such as: Halloween, Christmas, Sport,...
    def parse(self, response):
        themes = []
        for theme in response.css("a.m-explore-nav__link[href^='/t-shirts/']"):
            name = (theme.css("span.link__content::text").get() or "").strip()
            href = theme.attrib.get("href")
            
            if not (name and href):
                continue
            url = add_or_replace_query_string(response.urljoin(href), sort="popular")
            component = {"name": name, "url": url}
            themes.append(component)
            self.logger.info(f"Teepublic: Crawling theme - {name}")
            yield response.follow(url, callback=self.parse_theme, cb_kwargs={"theme": component})
    
    def parse_theme(self, response, theme):
        current_page = get_page_num(response.url)
        self.logger.info(f"Teepublic: Crawling theme - {theme['name']}, page number - {current_page}")
        product_endpoint = helper.extract_product_endpoint(response)
        self.logger.info(f"Teepublic: Product link - {product_endpoint}")
        for index, href in enumerate(product_endpoint, start=1):
            yield response.follow(
                response.urljoin(href),
                callback=self.parse_product,
                cb_kwargs={
                    "theme": theme,
                    "popular_page": current_page,
                    "popular_index": index,
                }
            )
        
        # Recursion to the next page
        next_href = extract_next_href(response)
        if next_href:
            next_url = add_or_replace_query_string(response.urljoin(next_href), sort="popular")
            yield response.follow(next_url, callback=self.parse_theme, cb_kwargs={"theme": theme})

    def parse_product(self, response, theme, popular_page, popular_index):
        product_response_url = response.url

        design_id = helper.extract_design_id(product_response_url, response)
        _, name = helper.extract_title_and_name(response)
        category_label = helper.extract_category_label(product_response_url, response)
        price = helper.extract_price(response)
        product_image = helper.get_image_from_id(response, design_id, os.getenv("SAVING_PATH"))
        artist_applied_tags = helper.extract_artist_applied_tags(response)
        trending_tags = helper.extract_trending_tags(response)

        yield ProductItem(
            id=design_id,
            name=name,
            category=category_label,
            primary_tag=theme.get("name"),
            product_url=product_response_url,
            price=price,
            product_image_path=product_image,
            artist_applied_tags=artist_applied_tags,
            trending_tags=trending_tags,
            popular_page=popular_page,
            popular_position=popular_index,
        )
