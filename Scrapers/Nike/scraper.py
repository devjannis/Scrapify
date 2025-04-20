import requests
import logging
from models import *


class Scraper:
    # List of channel IDs to try (some products are only listed in specific channels)
    CHANNEL_IDS = [
        "d9a5bc42-4b9c-4976-858a-f159cf99c647",  # nike.com and nike app
        "010794e5-35fe-4e32-aaff-cd2c74f89d61",  # snkrs web (launch.nike.com)
        "008be467-6c78-4079-94f0-70e2d6cc4003",  # snkrs app
    ]

    # Base URL of Nike API
    BASE_URL = "https://api.nike.com/product_feed/threads/v2"

    # Region information: language, marketplace code, and currency
    REGIONS = {
        "DE": {"language": "de", "marketplace": "DE", "currency": "€"},
        "CH": {"language": "de", "marketplace": "CH", "currency": "CHF"},
        "US": {"language": "en", "marketplace": "US", "currency": "$"},
        "LU": {"language": "de", "marketplace": "LU", "currency": "LUF"},
        "JP": {"language": "ja", "marketplace": "JP", "currency": "¥"},
        "BE": {"language": "de", "marketplace": "BE", "currency": "€"},
        "AT": {"language": "de", "marketplace": "AT", "currency": "€"},
        "PL": {"language": "pl", "marketplace": "PL", "currency": "zł"},
        "IT": {"language": "it", "marketplace": "IT", "currency": "€"},
        "FR": {"language": "fr", "marketplace": "FR", "currency": "€"},
        "NL": {"language": "nl", "marketplace": "NL", "currency": "€"},
        "UK": {"language": "en-gb", "marketplace": "GB", "currency": "£"},
        "AU": {"language": "en-gb", "marketplace": "AU", "currency": "$"},
        "CA": {"language": "en-gb", "marketplace": "CA", "currency": "$"},
        "ES": {"language": "en-gb", "marketplace": "ES", "currency": "€"},
        "SE": {"language": "en-gb", "marketplace": "SE", "currency": "kr"},
        "PT": {"language": "en-gb", "marketplace": "PT", "currency": "€"},
        "CZ": {"language": "en-gb", "marketplace": "CZ", "currency": "Kč"},
        "FI": {"language": "en-gb", "marketplace": "FI", "currency": "€"},
        "SI": {"language": "en-gb", "marketplace": "SI", "currency": "€"},
        "GR": {"language": "el-GR", "marketplace": "GR", "currency": "€"},
    }

    def __init__(self, region, sku):
        self.region = region.upper()
        self.sku = sku

    def _fetch(self):
        """
        Sends a GET request to fetch data from the API.
        
        Returns:
            dict: JSON response from the API if successful, else None.
        """
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            }
            filters = f"filter=language({self.REGIONS[self.region]['language']})&filter=marketplace({self.REGIONS[self.region]['marketplace']})&filter=productInfo.merchProduct.styleColor({self.sku})"
            for channel_id in self.CHANNEL_IDS:
                url = f"{self.BASE_URL}?{filters}&filter=channelId({channel_id})"
                response = requests.get(url=url, headers=header)
                response.raise_for_status()
                data = response.json()
                if data["pages"]["totalResources"] > 0:
                    return data
            else:
                raise Exception("No resources found for any channel ID")
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None

    @staticmethod
    def _parse_response(response_data):
        def _parse_variants(variants_data):
            return Variant(
                pid=variants_data["id"],
                group=variants_data["merchGroup"],
                gtin=variants_data["gtin"],
                size=variants_data["nikeSize"],
            )

        def _parse_availability_variants(variants_data):
            return AvailabilityVariant(
                pid=variants_data["id"],
                available=variants_data["available"],
                level=variants_data["level"],
            )

        product_info = response_data["objects"][0]["productInfo"][0]
        return Product(
            name=product_info["merchProduct"]["labelName"],
            sku=product_info["merchProduct"]["styleColor"],
            price=product_info["merchPrice"]["currentPrice"],
            discounted=product_info["merchPrice"]["discounted"],
            currency=product_info["merchPrice"]["currency"],
            channels=product_info["merchProduct"]["channels"],
            genders=product_info["merchProduct"]["genders"],
            quantity_limit=product_info["merchProduct"]["quantityLimit"],
            publish_type=product_info["merchProduct"]["publishType"],
            exclusive_access=product_info["merchProduct"]["exclusiveAccess"],
            commerce_start_date=product_info["merchProduct"]["commerceStartDate"],
            availability_variants=[
                _parse_availability_variants(av) for av in product_info["availableSkus"]
            ],
            variants=[_parse_variants(v) for v in product_info["skus"]],
        )

    def scrape_data(self):
        data = self._fetch()
        if data is None:
            return None
        parsed_data = self._parse_response(data)
        return parsed_data


if __name__ == "__main__":
    scraper = Scraper("de", "CW2288-111")
    product = scraper.scrape_data()
