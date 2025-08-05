DB_PATH = '/app/data/data.db'  # Update this when working on local
CHECK_INTERVAL_SECONDS = 600  # Check every 10 minutes

# API Configuration
API_URL = 'https://shop.amul.com/api/1/entity/ms.products?fields[name]=1&fields[brand]=1&fields[categories]=1&fields[collections]=1&fields[alias]=1&fields[sku]=1&fields[price]=1&fields[compare_price]=1&fields[original_price]=1&fields[images]=1&fields[metafields]=1&fields[discounts]=1&fields[catalog_only]=1&fields[is_catalog]=1&fields[seller]=1&fields[available]=1&fields[inventory_quantity]=1&fields[net_quantity]=1&fields[num_reviews]=1&fields[avg_rating]=1&fields[inventory_low_stock_quantity]=1&fields[inventory_allow_out_of_stock]=1&fields[default_variant]=1&fields[variants]=1&fields[lp_seller_ids]=1&filters[0][field]=categories&filters[0][value][0]=protein&filters[0][operator]=in&filters[0][original]=1&facets=true&facetgroup=default_category_facet&limit=24&total=1&start=0'

# Headers and Cookies
API_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-US;q=0.6',
    'base_url': 'https://shop.amul.com/en/browse/protein',
    'dnt': '1',
    'frontend': '1',
    'priority': 'u=1, i',
    'referer': 'https://shop.amul.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'tid': '1754375005083:262:a6a7b853bf6d9c50d123842f2911a7a6e38f4a650c89cb64d745e165d9d8ff1f',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

API_COOKIES = {
    '_fbp': 'fb.1.1746962099270.834512015416653601',
    '_ga': 'GA1.1.642699511.1746962100',
    'jsessionid': 's%3ANXqLZFP5KUJk0Qqe3tZ6a6sz.M0sD7o3GiCa%2Fhcx%2F5c2f9ZNGskWAYOnNohkzTHgHj2U',
    '__cf_bm': 'AtgNZU9UKIU2nRebGZ34yuGTNMvSln2Qg4EwA5IcUeA-1754374984-1.0.1.1-B76Ar.oWehikT.ZoLavaVATLVNr3r_hbNq2uMaEn3zTFcRb1AlHtbgUDH.4GKVpk.sPiCW4cqG90.QrEhE6TWkZg7tAo3nDFJzlejZYsu7M',
    '_ga_E69VZ8HPCN': 'GS2.1.s1754374985$o12$g1$t1754375006$j39$l0$h656146599',
}
