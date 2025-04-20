import requests
import logging
from models import *

class Scraper:
    BASE_URL = "https://api.snipes.com/sni-pl-prd-stor-we-char/v1/v1/products/"
    
    def __init__(self, pid):
        self.bearer = "" # snipes api bearer for api access, retrieve it by using the chrome dev tool
        
        self.pid = pid # Product ID to scrape
        
    def _get_url(self):
        return self.BASE_URL + self.pid
    
    def _get_headers(self):        
        return {
            'sec-ch-ua-platform': '"macOS"',
            'Referer': '',
            'sec-ch-ua': '"Chromium";v="135", "Not-A.Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'X-Charybdis': self.bearer, # Bearer token is sent as a custom header. If request fails replace it!
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'DNT': '1',
        }
    
    def _fetch(self):
        try:
            headers = self._get_headers() # Get headers
            url = self._get_url() # Build url
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json() # Return response data as JSON
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None # Return None if request fails
    
    @staticmethod
    def _parse_response(product_data):
        # Parse stock data for a variant
        def parse_stock(stock_data):
            return Stock(
                supplier_id=stock_data['supplierId'],
                warehouse_id=stock_data['warehouseId'],
                quantity=stock_data['quantity'],
                sellable_without_stock=stock_data['isSellableWithoutStock']
            )
            
        # Parse variant information
        def _parse_variant(variant_data):
            return Variant(
                pid=variant_data['id'],
                stock=parse_stock(variant_data['stock']),
                price=variant_data['price']['formatted'],
                size=variant_data['sizeMap']['size']['value']
            )
        
        # Build image link and return Image object
        def _parse_image(image_data):
            link = f"https://asset.snipes.com/images/f_auto,q_100,d_fallback-sni.png/b_rgb:f8f8f8,c_pad,w_680,h_680/dpr_1.0/{image_data['public_id']}/image"
            
            return Image(
                id=image_data['public_id'],
                link=link,
            )
        
        # Convert price from cents to euro
        def _parse_price(price_data):
            min_price = price_data['min']['withTax'] / 100
            max_price = price_data['max']['withTax'] / 100
            
            return Price(
                min=str(min_price),
                max=str(max_price)
            )
            
        # Extract deep link URI from nested data
        uri = (product_data.get('advancedAttributes', {})
                    .get('productDeepLink', {})
                    .get('values', [{}])[0]
                    .get('fieldSet', [{}])[0][0]
                    .get('value', 'www.snipes.com/'))
        
        # Construct Product object from data
        return Product(
            pid=product_data['id'],
            sku=product_data['attributes']['manufacturerCode']['values']['label'],
            name=product_data['attributes']['name']['values']['label'],
            price=_parse_price(product_data['priceRange']),
            uri = "https://" + uri,
            active=product_data['isActive'],
            new=product_data['isNew'],
            sold_out=product_data['isSoldOut'],
            masterKey=product_data['masterKey'],
            hot_relase=product_data['attributes']['isHotRelease']['values']['value'],
            color=product_data['attributes']['color']['values']['label'],
            brand=product_data['attributes']['brand']['values']['label'],
            release_date_time=product_data['firstLiveAt'],
            images=[_parse_image(i) for i in product_data['images']],
            variants=[_parse_variant(v) for v in product_data['variants']]
            
        )
            
    def scrape_data(self):
        data = self._fetch() # Get data from API
        if data is None:
            return None # Return None if fetch failed
        return self._parse_response(data) # Parse and return product object
        
if __name__ == "__main__":
    scraper = Scraper("24853") # Initialize scraper
    product = scraper.scrape_data() # Test scraper