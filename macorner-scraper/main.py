import os
import csv
import requests
from dotenv import load_dotenv
from constants import REVIEW_PRODUCT_URL_TEMPLATE, CSV_PATH, PRODUCTS_PER_PAGE
from review import Review

def write_reviews_csv(path: str, reviews: list[Review]) -> None:
    if not reviews:
        print("No reviews to write.")
        return

    # Convert models -> rows (and stringify picture_urls for CSV)
    rows = []
    for rv in reviews:
        row = rv.model_dump()
        # join list of URLs into a single string (use ' | ' as separator)
        row["picture_urls"] = " | ".join(row.get("picture_urls") or [])
        rows.append(row)

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    file_exists = os.path.exists(path)
    fieldnames = list(rows[0].keys())

    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerows(rows)

load_dotenv()
while True:
    product_url = input("Please input url: ").strip()
    if product_url.lower() == "q" or not product_url:
        break
    max_page = int(input("Please input max number of page to crawl review: ").strip())
    
    try:
        # 1) Get product info
        resp = requests.get(product_url.rstrip("/") + ".json", timeout=15)
        resp.raise_for_status()
        data = resp.json()

        product_info = data.get("product")
        if not product_info:
            print("Could not find 'product' in response JSON. Is this a valid product URL?")
            continue

        product_id = product_info.get("id")
        if not product_id:
            print("Product JSON missing 'id'.")
            continue

        models: list[Review] = []
        for page in range(1, max_page + 1):
            review_response = requests.get(
                REVIEW_PRODUCT_URL_TEMPLATE.format(
                    external_id_template=str(product_id),
                    number_of_prods = PRODUCTS_PER_PAGE,
                    page_num = page
                    ), 
                timeout=20
                )
            review_response.raise_for_status()
            items = review_response.json().get("reviews") or []

            if not items:
                print("No reviews found.")
                continue

            # 3) Map to your Pydantic model
            for it in items:
                obj = Review.from_judgeme(
                    it,
                    product_url_input=product_url,
                    product_id=str(product_id),
                )
                models.append(obj)

            # 4) Write to CSV
        write_reviews_csv(CSV_PATH, models)

    except requests.exceptions.RequestException as e:
        print(f"Network/HTTP error: {e}")
    except ValueError:
        print("Response was not valid JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")
