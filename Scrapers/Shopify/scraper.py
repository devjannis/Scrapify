import requests
import logging
from models import *


class Scraper:

    def __init__(self, url):
        self.base_url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }

    def _fetch(self, url):
        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Wirft Fehler wenn Status != 200
            return response.json()  # Gibt JSON-Antwort zurück
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None

    @staticmethod
    def _parse_response(product_data):

        # Bilder in richtige Objekte packen
        def _parse_image(img):
            return Image(
                id=img["id"],
                position=img["position"],
                created_at=img["created_at"],
                updated_at=img["updated_at"],
                alt=img.get("alt"),
                width=img["width"],
                height=img["height"],
                src=img["src"],
                variant_ids=img["variant_ids"],
            )

        # Parse product option data
        def _parse_option(opt):
            return Option(
                id=opt["id"],
                name=opt["name"],
                position=opt["position"],
                values=opt["values"],
            )

        # Parse quantity rule data
        def _parse_quantity_rule(qr):
            return QuantityRule(
                min=qr["min"], max=qr.get("max"), increment=qr["increment"]
            )

        # Parse product variant data
        def _parse_variant(var):
            return Variant(
                id=var["id"],
                title=var["title"],
                price=var["price"],
                sku=var["sku"],
                position=var["position"],
                barcode=var["barcode"],
                weight=var["weight"],
                weight_unit=var["weight_unit"],
                taxable=var["taxable"],
                requires_shipping=var["requires_shipping"],
                quantity_rule=_parse_quantity_rule(var["quantity_rule"]),
                price_currency=var["price_currency"],
            )

        # Extract and map product fields
        product = product_data["product"]
        return Product(
            id=product["id"],
            title=product["title"],
            vendor=product["vendor"],
            product_type=product["product_type"],
            handle=product["handle"],
            tags=product["tags"],
            image=_parse_image(product["image"]),
            options=[_parse_option(o) for o in product["options"]],
            images=[_parse_image(i) for i in product["images"]],
            variants=[_parse_variant(v) for v in product["variants"]],
        )

    def scrape_data(self):
        data = self._fetch(self.base_url + ".json")  # Fetch JSON from URL
        if data is None:
            return None
        parsed_data = self._parse_response(data)  # Convert to Product object
        return parsed_data


if __name__ == "__main__":
    scraper = Scraper(
        "https://funkoeurope.com/products/darth-vader-vs-luke-skywalker-star-wars-return-of-the-jedi"
    )

    product = scraper.scrape_data()
