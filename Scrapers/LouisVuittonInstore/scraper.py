import requests
from models import *
import logging

class Scraper:
    def __init__(self, pid, city=""):
        self.city = city
        self.pid = pid

    def _get_headers(self) -> dict:
        return {
            "Host": "api.louisvuitton.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Site": "same-site",
            "Accept-Language": "de-DE,de;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "Origin": "https://de.louisvuitton.com",
            "client_id": "607e3016889f431fb8020693311016c9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)",
            "Referer": "https://de.louisvuitton.com/deu-de/zur-kasse/voraussichtl-versandkosten?lvpass=true&lvpassdesign=true",
            "client_secret": "60bbcdcD722D411B88cBb72C8246a22F",
            "Sec-Fetch-Dest": "empty",
            "Content-Type": "application/json",
        }

    def _get_mobile_headers(self) -> dict:
        return {
            "Host": "pass-api.louisvuitton.com",
            "Accept": "*/*",
            "User-Agent": "LVapp/ios/6.40.1.17199 LVApp PRD",
            "Accept-Language": "de-DE,de;q=0.9",
            "Connection": "keep-alive",
        }

    def _get_params(self) -> dict:
        return {
            "locale": "de_DE",
        }

    def _fetch_mobile(self) -> dict:
        params = self._get_params()
        headers = self._get_mobile_headers()
        response = requests.get(
            f"https://pass-api.louisvuitton.com/api/catalog/product/{self.pid}",
            params=params,
            headers=headers,
        )
        return response.json()

    def _fetch(self, url, json_data) -> dict:
        try:
            headers = self._get_headers()
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Scrape failed: {e}")
            return None

    @staticmethod
    def _parse_product(product_data) -> Product:

        def _parse_sku(sku_data) -> Sku:

            def _parse_store(store_data) -> Store:

                def _parse_geo_location(geo_data) -> GeoLocation:
                    return GeoLocation(
                        latitude=geo_data.get("latitude", "N/A"),
                        longitude=geo_data.get("longitude", "N/A"),
                    )

                def _parse_address(address_data) -> Address:
                    return Address(
                        street=address_data.get("streetAddress", "N/A"),
                        postal_code=address_data.get("postalCode", "N/A"),
                        city=address_data.get("addressLocality", "N/A"),
                        country=address_data.get("addressCountry", "N/A"),
                    )

                def _parse_working_hours(working_data) -> WorkingHours:
                    return WorkingHours(
                        day_of_week=working_data["dayOfWeek"],
                        opens=working_data["opens"],
                        closes=working_data["closes"],
                    )

                def _parse_propertys(property_data) -> Propertys:
                    is_available = False
                    is_flagship = False
                    is_available_for_cc = False
                    is_display_locate_in_store = False
                    estimated_cc_delivery_date = None
                    for property in property_data:
                        if property["name"] == "stockAvailability":
                            is_available = property["value"]
                        elif property["name"] == "flagship":
                            is_flagship = property["value"]
                        elif property["name"] == "availableForCC":
                            is_available_for_cc = property["value"]
                        elif property["name"] == "displayLocateInStore":
                            is_display_locate_in_store = property["value"]
                        elif property["name"] == "clickAndCollect":
                            estimated_cc_delivery_date = (
                                property["value"]
                                .get("estimatedDeliveryDate", {})
                                .get("time", None)
                            )

                    return Propertys(
                        available=is_available,
                        flagship=is_flagship,
                        available_for_cc=is_available_for_cc,
                        display_locate_in_store=is_display_locate_in_store,
                        estimated_delivery_date=estimated_cc_delivery_date,
                    )

                return Store(
                    name=store_data.get("name", "N/A"),
                    telephone=store_data.get("telephone", "N/A"),
                    identiefer=store_data.get("identifier", "N/A"),
                    brand=store_data.get("brand"),
                    geo=_parse_geo_location(store_data.get("geo", {})),
                    url=store_data.get("url", "N/A"),
                    address=_parse_address(store_data.get("address", {})),
                    image=store_data.get("image", [])[0].get("contentUrl", "N/A"),
                    working_hours=[
                        _parse_working_hours(working_data)
                        for working_data in store_data.get("hoursAvailable", [])
                    ],
                    propertys=_parse_propertys(
                        store_data.get("additionalProperty", {})
                    ),
                )

            return Sku(
                sku=sku_data.get("skuId", "N/A"),
                name=sku_data.get("name", "N/A"),
                size=sku_data.get("size", "N/A"),
                stores=[
                    _parse_store(store_data) for store_data in sku_data.get("store", {})
                ],
                color=sku_data.get("color", "N/A"),
                image=sku_data.get("mediaUrl", "N/A"),
            )

        return Product(
            name=product_data.get("name", "N/A"),
            sku=product_data.get("sku", "N/A"),
            product_id=product_data.get("productId", "N/A"),
            link=product_data.get("webPath", "N/A"),
            skus=[_parse_sku(sku_data) for sku_data in product_data.get("skus", [])],
            is_back_order=product_data.get("isBackOrder", "N/A"),
            sellable_status=product_data.get("sellableStatus", {}).get(
                "sellable", "N/A"
            ),
            price=product_data.get("sellableStatus", {})
            .get("price", {})
            .get("price", "N/A"),
            apple_pay_enabled=product_data.get("isApplePayEnabled", "N/A"),
        )

    def scrape_data(self) -> Product:
        data = self._fetch_mobile()

        for variant in data["skus"]:
            json_data = {
                "country": "DE",
                "query": self.city,
                "clickAndCollect": False,
                "skuId": variant["skuId"],
                "pageType": "buypath",
            }
            response = self._fetch(
                url="https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/deu-de/stores/query",
                json_data=json_data,
            )
            variant["store"] = response.get("hits", [])

        return self._parse_product(data)

if __name__ == "__main__":
    scraper = Scraper("M13676")
    embed = scraper.scrape_data()
