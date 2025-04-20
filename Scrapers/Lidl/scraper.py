import requests
from models import *
import logging
from typing import Optional

class Scraper:
    BASE_URL = "https://www.lidl.de/p/api/gridboxes/DE/de?erpNumbers="
    
    def __init__(self, pid):
        self.pid = pid
     
    @staticmethod  
    def _parse_response(response_data) -> Product:
        def _parse_brand(brand_data) -> Brand:
            return Brand(
                logo=brand_data['logo'],
                name=brand_data['name'],
                url=brand_data['url'],
                pid=brand_data['id'],
                show=brand_data['showBrand']
            )
        
        discounted = response_data.get('price', {}).get('discount', False)
        if discounted:
            discounted = True
        
        return Product(
            pid=response_data.get('productId', 'N/A'),
            ians=response_data.get('ians'),
            product_type=response_data.get('productType', 'N/A'),
            rating=response_data.get('ratings', {}).get('average', 0.0),
            title=response_data.get('title', 'N/A'),
            price=response_data.get('price', {}).get('price', 0),
            discounted=discounted,
            discount=response_data.get('price', {}).get('discount', {}).get('percentageDiscount', 0),
            old_price=response_data.get('price', {}).get('discount', {}).get('deletedPrice', None),
            images=response_data.get('imageList'),
            brand=_parse_brand(response_data.get('brand', {}))
        )
        
    def _fetch(self) -> Optional[dict]:
        try:
            response = requests.get(self.BASE_URL + self.pid)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None
    
    def scrape_data(self) -> Optional[Product]:
        data = self._fetch()
        if data is None:
            return None
        parsed_data = self._parse_response(data[0])
        return parsed_data
    
if __name__ == "__main__":
    scraper = Scraper("100270851")
    print(scraper.scrape_data())