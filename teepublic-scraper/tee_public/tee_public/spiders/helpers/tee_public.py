from __future__ import annotations
from typing import List, Dict, Optional, Tuple
import re
from tee_public.spiders.constant import MONEY_RE, CLOUDINARY_RE, SELECTOR, RUDDER_IMG_RE
import os
from dotenv import load_dotenv
import requests
from urllib.parse import unquote
from pathlib import Path

load_dotenv()
PRODUCT_URL_TEMPLATE = (os.getenv("PRODUCT_URL_TEMPLATE"))

_PRODUCT_URL_ID_RE = re.compile(
    r"/(?:t-shirt|hoodie|tank-top|crewneck-sweatshirt|baseball-t-shirt|long-sleeve-t-shirt)/(\d+)"
)

def extract_design_id(url: str, response) -> Optional[str]:
    m = _PRODUCT_URL_ID_RE.search(url)
    if m:
        return m.group(1)
    # fallback: visible "Design ID:"
    txt = response.xpath(
        "normalize-space(//text()[contains(., 'Design ID:')]/following::text()[1])"
    ).get()
    if txt:
        m2 = re.search(r"\d+", txt)
        return m2.group(0) if m2 else None
    return None

# --- Title / Name -------------------------------------------------------------

def extract_title_and_name(response) -> Tuple[str, str]:
    raw_title = (response.css(SELECTOR["title"]).get() or "").strip()
    if not raw_title:
        return "", ""
    # name is title without trailing category token
    name = re.sub(
        r"\s+(T-?Shirt|Hoodie|Tank Top|Crewneck Sweatshirt|Baseball T-?Shirt|Long Sleeve T-?Shirt)$",
        "",
        raw_title,
        flags=re.I,
    ).strip() or raw_title
    return raw_title, name

# --- Category ----------------------------------------------------------------

def extract_category_label(url: str, response) -> str:
    pm = re.search(
        r"/(t-shirt|hoodie|tank-top|crewneck-sweatshirt|baseball-t-shirt|long-sleeve-t-shirt)/",
        url, re.I
    )
    cat_from_url = pm.group(1) if pm else None
    raw_h2 = (response.css("h2::text").get() or "").lower()
    return cat_from_url or raw_h2

# --- Price -------------------------------------------------------------------

def extract_price(response) -> Optional[str]:
    for selector in SELECTOR["price_candidates"]:
        val = response.css(selector).get()
        if val:
            m = MONEY_RE.search(val.replace(",", ""))
            return m.group(1) if m else val
    return None

# --- Images ------------------------------------------------------------------

def extract_product_image(response) -> Optional[str]:
    """
    Extract the primary product image from a Teepublic product page.
    Looks only at the `design_image_url` key in the embedded script payload.
    """
    m = RUDDER_IMG_RE.search(response.text)
    if m:
        return unquote(m.group(1))
    return None

# --- Tags --------------------------------------------------------------------

def _collect_tag_links(block, response) -> List[Dict[str, str]]:
    out = []
    for a in response.css(block):
        txt = (a.css(SELECTOR["tag_text"]).get() or "").strip()
        href = a.attrib.get("href") or a.attrib.get("data-href")
        if txt and href:
            out.append({"text": txt, "href": response.urljoin(href.strip())})
    return out

def extract_artist_applied_tags(response) -> List[Dict[str, str]]:
    return _collect_tag_links(SELECTOR["artists_tags_block"], response)

def extract_trending_tags(response) -> List[Dict[str, str]]:
    return _collect_tag_links(SELECTOR["trending_tags_block"], response)

# --- Listing helpers ----------------------------------------------------------

def extract_product_endpoint(response) -> List[str]:
    for selector in SELECTOR["product_card_links"]:
        links = response.css(selector).getall()
        if links:
            return links
    return []

def extract_next_href(response) -> Optional[str]:
    return response.css(SELECTOR["rel_next"]).get()


def get_image_from_id(response, design_id, saving_path):
    # ensure saving_path is a folder
    saving_path = Path(saving_path)
    saving_path.mkdir(parents=True, exist_ok=True)

    # Try template URL first
    url = PRODUCT_URL_TEMPLATE.format(id=design_id)
    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
    except Exception:
        # fallback
        url = extract_product_image(response)
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()

    # detect extension from Content-Type header
    content_type = resp.headers.get("Content-Type", "").lower()
    if "png" in content_type:
        ext = ".png"
    elif "jpeg" in content_type or "jpg" in content_type:
        ext = ".jpg"

    filename = f"{design_id}{ext}"
    filepath = saving_path / filename

    # write file
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)

    return url