from dotenv import load_dotenv
import os
load_dotenv()

PRODUCTS_PER_PAGE = os.getenv("PRODUCTS_PER_PAGE")
CSV_PATH = os.getenv("CSV_PATH")
EXTERNAL_ID_TEMPLATE = "external_id_template"
REVIEW_PRODUCT_URL_TEMPLATE = os.getenv("REVIEW_PRODUCT_URL_TEMPLATE")
