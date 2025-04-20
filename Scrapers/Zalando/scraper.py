import requests
import logging
from models import *

class Scraper:
    REGIONS = { # Zalando region endpoints
        "de": "www.zalando.de",
        "uk": "www.zalando.co.uk",
        "at": "www.zalando.at",
        "be": "www.zalando.be",
        "ch": "www.zalando.ch",
        "pl": "www.zalando.pl",
        "fr": "www.zalando.fr",
        "it": "www.zalando.it",
        "nl": "www.zalando.nl",
        "es": "www.zalando.es",
        "se": "www.zalando.se",
        "dk": "www.zalando.dk",
        "no": "www.zalando.no",
        "ie": "www.zalando.ie",
        "pt": "www.zalando.pt",
        "cz": "www.zalando.cz",
        "si": "www.zalando.si",
        "fi": "www.zalando.fi",
    }

    def __init__(self, pid, region):
        self.pid = pid.upper() # Make PID uppercase (needed for endpoint)
        self.url = self._get_region_url(region) # Get correct region endpoint
        self.endpoint = self.url + "/api/graphql/mobile" # API endpoint

    def _get_region_url(self, region):
        region = region.lower()
        if region not in self.REGIONS:
            logging.error(f"Invalid region: {region}")
            raise ValueError(f"Invalid region: {region}")
        return self.REGIONS[region] # Return the region URL

    def _get_headers(self):
        return { # Headers mimic Zalando iPad app
            "Host": self.url,
            "User-Agent": "zalando/25.7.0 (iPad; iOS 18.4; Scale/2.00)",
            "x-zalando-feature": "pdp",
            "X-Logged-In": "true",
            "X-device-Type": "tablet",
            "X-Frontend-Type": "mobile-app",
            "X-APOLLO-OPERATION-NAME": "PdpRelevantEntities",
            "X-device-OS": "ios",
            "x-os-version": "18.4",
            "x-zalando-intent-context": "navigationTargetGroup=WOMEN",
            "Connection": "keep-alive",
            "x-device-platform": "ios",
            "Accept": "application/json",
            "X-APOLLO-OPERATION-TYPE": "query",
            "Content-Type": "application/json",
        }

    def _get_data(self):
        return { # GraphQL query data
            "id": "46683e61c8b7d4fda6e21da37d67a89f0a7b8a2848460110b3b48576dce9ea92",
            "operationName": "Pdp",
            "variables": {
                "beautyColorImageWidth": 1,
                "benefitsLogoWidth": 84,
                "brandedBarLogoWidth": 300,
                "brandLogoWidth": 800,
                "colorImageWidth": 76,
                "configSku": self.pid, # product ID
                "experienceLogoWidth": 300,
                "fullScreenGalleryWidth": 1200,
                "fullScreenHdGalleryWidth": 2600,
                "maxFlagCount": 3,
                "portraitGalleryWidth": 1170,
                "segmentedBannerHeaderLogoWidth": 108,
                "shouldIncludeFlagInfo": False,
                "shouldIncludeHistogramValues": False,
                "shouldIncludeOfferSelectionValues": False,
                "shouldIncludeOmnibusConfigModeChanges": False,
                "shouldIncludeOmnibusPrice": False,
                "shouldIncludePrestigeBeauty": False,
                "shouldIncludePurchaseRestriction": False,
                "shouldIncludeReleaseDate": True,
                "shouldIncludeSamples": False,
                "shouldIncludeSegmentation": False,
                "shouldIncludeSegmentGatedComingSoonReminder": True,
                "shouldIncludeSizeAdvicewBM": False,
                "shouldIncludeSubscriptionValues": False,
                "shouldIncludeSustainabilityClaims": False,
                "shouldIncludeTargetedCoupons": True,
                "shouldIncludeUSPReturnPolicy": False,
            },
        }

    def _fetch(self):
        try:
            headers = self._get_headers() # Get request headers
            data = self._get_data() # Get request data
            response = requests.post(
                url="https://" + self.endpoint, json=data, headers=headers, timeout=10
            )
            response.raise_for_status() # Raise error if status not 200
            return response.json() # Return response data as JSON
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None # Return nothing if it fails

    @staticmethod
    def _parse_response(product_data):
        # Parse price data
        def _parse_price(price_data):
            return Price(value=price_data["original"]["formatted"])

        # Parse stock data
        def _parse_stock(stock_data):
            return Stock(quantity=stock_data["quantity"])

        # Parse offer data
        def _parse_offer(offer_data):
            return Offer(
                price=_parse_price(offer_data["price"]),
                stock=_parse_stock(offer_data["stock"]),
            )
            
        # Parse variant data
        def _parse_variant(variant_data):
            return Variant(
                size=variant_data["size"],
                sku=variant_data["sku"],
                supplierSize=variant_data["supplierSize"],
                offer=_parse_offer(variant_data["offer"]),
            )

        # Parse brand data
        def _parse_brand(brand_data):
            return Brand(name=brand_data["name"], id=brand_data["id"])

        # Parse color data
        def _parse_color(color_data):
            return Color(name=color_data["name"])

        # Parse image data
        def _parse_image(image_data):
            return Image(uri=image_data["media"].get("uri", None))

        # Build the Product object
        return Product(
            sku=product_data["data"]["product"]["sku"],
            name=product_data["data"]["product"]["name"],
            uri=product_data["data"]["product"]["uri"],
            group=product_data["data"]["product"]["group"],
            comingSoon=product_data["data"]["product"]["comingSoon"],
            isActive=product_data["data"]["product"]["isActive"],
            brand=_parse_brand(product_data["data"]["product"]["brand"]),
            color=_parse_color(product_data["data"]["product"]["color"]),
            price=_parse_price(product_data["data"]["product"]["displayPrice"]),
            variants=[
                _parse_variant(v)
                for v in product_data["data"]["product"].get("simples", [])
            ],
            images=[
                _parse_image(i)
                for i in product_data["data"]["product"].get(
                    "fullScreenHdGalleryMedia", []
                )
            ],
        )

    def scrape_data(self):
        data = self._fetch() # Fetch data
        if data is None:
            return None
        return self._parse_response(data) # Parse and return

if __name__ == "__main__":
    scraper = Scraper(pid="lls42e00y-q11", region="de") # Initialize scraper with PID and region
    product = scraper.scrape_data() # Run scraping
