import requests
import logging
from models import *
from typing import Optional

class Scraper:
    BASE_URL = (
        "https://searchserverapi.com/getwidgets?api_key=3c7s6k4F2C&_=ci&maxResults=1&q="
    )
    STORE_URL = "https://eu.kith.com/"

    def __init__(self, pid):
        self.pid = pid

    def _get_url(self) -> str:
        return self.BASE_URL + self.pid

    @staticmethod
    def _get_headers() -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        }

    def _fetch(self) -> Optional[dict]:
        try:
            endpoint = self._get_url()
            headers = self._get_headers()
            response = requests.get(url=endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None

    def _parse_response(self, product_data) -> Product:
        # Parse the product variant information
        def _parse_variant(variant_data) -> Variant:
            return Variant(
                pid=variant_data["variant_id"],
                sku=variant_data["sku"],
                price=variant_data["price"],
                size=variant_data["options"]["Size"],
                quantity=variant_data.get("quantity_total", "0"),
                link=self.STORE_URL + variant_data["link"],
            )

        # Parse the product information
        return Product(
            pid=product_data.get("product_id", "UNKNOWN"),
            sku=product_data["product_code"],
            title=product_data["title"],
            description=product_data["description"],
            link=self.STORE_URL + product_data["link"],
            price=product_data["price"],
            image=product_data["image_link"],
            vendor=product_data["vendor"],
            discount=product_data["discount"],
            total_reviews=product_data["total_reviews"],
            images=product_data["shopify_images"],
            variants=[_parse_variant(v) for v in product_data["shopify_variants"]],
        )

    def scrape_data(self) -> Optional[Product]:
        data = self._fetch()
        if data is None:
            return None
        parsed_data = self._parse_response(data["items"][0])
        return parsed_data


if __name__ == "__main__":
    scraper = Scraper("aajs0727")
    print(scraper.scrape_data())
