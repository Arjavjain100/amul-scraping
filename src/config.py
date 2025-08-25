import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PINCODE = "248001"
DB_PATH = "/app/data/data.db"  # Update this to ./data/data.db when working on local
CHECK_INTERVAL_SECONDS = 600  # Check every 10 minutes

# API Configuration
API_URL = "https://shop.amul.com/api/1/entity/ms.products?fields[name]=1&fields[brand]=1&fields[categories]=1&fields[collections]=1&fields[alias]=1&fields[sku]=1&fields[price]=1&fields[compare_price]=1&fields[original_price]=1&fields[images]=1&fields[metafields]=1&fields[discounts]=1&fields[catalog_only]=1&fields[is_catalog]=1&fields[seller]=1&fields[available]=1&fields[inventory_quantity]=1&fields[net_quantity]=1&fields[num_reviews]=1&fields[avg_rating]=1&fields[inventory_low_stock_quantity]=1&fields[inventory_allow_out_of_stock]=1&fields[default_variant]=1&fields[variants]=1&fields[lp_seller_ids]=1&filters[0][field]=categories&filters[0][value][0]=protein&filters[0][operator]=in&filters[0][original]=1&facets=true&facetgroup=default_category_facet&limit=24&total=1&start=0"

# Email Configuration
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "True").lower() == "true"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_TO = (
    os.getenv("EMAIL_TO", "").split(",") if os.getenv("EMAIL_TO") else []
)  # Comma-separated emails
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Back in Stock")
