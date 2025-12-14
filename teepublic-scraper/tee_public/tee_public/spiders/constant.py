import re

CLOUDINARY_RE = re.compile(r"https?://(?:res\.)?cloudinary\.com/[^\s\"'<>)\]]+", re.I)
MONEY_RE = re.compile(r"(\d+(?:\.\d{1,2})?)")
RUDDER_IMG_RE = re.compile(r'"design_image_url"\s*:\s*"([^"]+)"', re.I)

# Common selectors (centralize so you tweak once if the site changes)
SELECTOR = {
    "nav_tshirt_links": "a.m-explore-nav__link[href^='/t-shirts/']",
    "nav_link_text": "span.link__content::text",
    "product_card_links": [
        "a.tp-design-tile__title_link::attr(href)",
        "a[data-testid='product-card-link']::attr(href)",
        "a.product-card__link::attr(href)",
    ],
    "rel_next": "link[rel='next']::attr(href)",
    "title": "h1::text, [data-testid='product-title']::text",
    "price_candidates": [
        "span[data-testid='regular-price']::text",
        "meta[itemprop='price']::attr(content)",
        "meta[property='product:price:amount']::attr(content)",
    ],
    "og_image": "meta[property='og:image']::attr(content)",
    "cloudinary_img": "img[src*='cloudinary']::attr(src)",
    "artists_tags_block": (
        "div.m-design__additional-info"
        "[data-rudderstack--link-clicked-location-value='related_tags_artists_applied_tags'] "
        "nav.m-design__additional-info-list a"
    ),
    "trending_tags_block": (
        "div.m-design__additional-info"
        "[data-rudderstack--link-clicked-location-value='related_tags_trending_tags'] "
        "nav.m-design__additional-info-list a"
    ),
    "tag_text": "span.link__content::text",
}
