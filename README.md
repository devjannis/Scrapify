# Retail Scrapers Collection - Scrapify

A collection of scrapers for various online retailers and e-commerce platforms. This library allows you to retrieve product data from popular websites like Nike, Zalando, Shopify, and more.

## Overview

This project provides a unified interface for retrieving product information from various online stores. Each scraper is implemented as a standalone module and can be used independently or in combination. The data is returned in structured Python objects and can optionally be formatted as Discord embeds.

## Features

- **Modular Design**: Each scraper is implemented in its own module
- **Unified API**: Consistent interface across different retailers
- **Discord Integration**: Direct conversion of product data to Discord embeds
- **Error Handling**: Robust error handling for API requests
- **Typed Data Structures**: Use of dataclasses for clearly defined data models

## Available Scrapers

| Retailer | Module | Description |
|--------------|-------|-------------|
| Nike | `Nike` | Nike online store and SNKRS app products |
| Zalando | `Zalando` | Zalando e-commerce platform with regional support |
| Snipes | `Snipes` | Sneakers and streetwear from Snipes |
| Shopify | `Shopify` | General Shopify store scraper (usable for any Shopify store) |
| Louis Vuitton | `LouisVuittonInstore` | In-store availability of Louis Vuitton products |
| Lego | `Lego` | Lego online store products |
| Lidl | `Lidl` | Lidl online store offerings |
| KithEU | `KithEU` | Kith EU online store products |

## Installation

To use this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/devjannis/Scrapify
cd Scrapify
pip install -r requirements.txt
```

### Dependencies

- Python 3.8+
- requests
- dataclasses
- discord.py (for embed functionality)
- pytz (for timezone conversion)

## Usage

Each scraper follows a similar usage pattern:

```python
from Scrapers import ExampleScraper

# Initialize the scraper with product ID and region
scraper = ExampleScraper("de", "CW2288-111")

# Retrieve the product data
product = scraper.scrape_data()

# Output product information
print(product)

# Optional: Generate a Discord embed
embed = product.to_embed()
```

### Example: Nike Scraper

```python
from Scrapers import NikeScraper

# Search for a Nike product with SKU
scraper = NikeScraper("de", "CW2288-111")
product = scraper.scrape_data()

# Display product information
print(f"Name: {product.name}")
print(f"SKU: {product.sku}")
print(f"Price: {product.price} {product.currency}")
print(f"Sizes: {[v.size for v in product.variants]}")

# Create Discord embed
embed = product.to_embed()
```

### Example: Zalando Scraper

```python
from Scrapers import ZalandoScraper

# Search for a Zalando product with PID
scraper = ZalandoScraper(pid="lls42e00y-q11", region="de")
product = scraper.scrape_data()

# Display product information
print(f"Name: {product.name}")
print(f"SKU: {product.sku}")
print(f"Brand: {product.brand.name}")
print(f"Variants: {len(product.variants)}")

# Create Discord embed
embed = product.to_embed()
```

### Example: Shopify Scraper

```python
from Scrapers import ShopifyScraper

# Retrieve a product from any Shopify store
scraper = ShopifyScraper("https://funkoeurope.com/products/darth-vader-vs-luke-skywalker-star-wars-return-of-the-jedi")
product = scraper.scrape_data()

# Display product information
print(f"Name: {product.title}")
print(f"Manufacturer: {product.vendor}")
print(f"Product Type: {product.product_type}")
```

## Project Structure

```
Scrapers/
├── __init__.py
├── KithEU/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── Lego/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── Lidl/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── LouisVuittonInstore/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── Nike/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── Shopify/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
├── Snipes/
│   ├── __init__.py
│   ├── models.py
│   └── scraper.py
└── Zalando/
    ├── __init__.py
    ├── models.py
    └── scraper.py
```

Each scraper module contains:

- **scraper.py**: The main class for retrieving and processing product data
- **models.py**: Data definitions with dataclasses for products, variants, and related entities
- **__init__.py**: Enables the module to be used as a Python package

## Contributions

Contributions are welcome! If you want to add a new scraper or improve an existing one do that!

## Adding a New Scraper

To add a new scraper, create a new directory within the `Scrapers` folder and implement the following files:

1. `models.py` with the required dataclasses
2. `scraper.py` with a Scraper class that implements at least the following methods:
   - `__init__`: Constructor to initialize the scraper
   - `_fetch`: Method to retrieve raw data
   - `_parse_response`: Method to parse the response into model objects
   - `scrape_data`: Public method for querying and processing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is intended for educational and research purposes only. Please respect the terms of service of respective websites before using these scrapers. The author assumes no responsibility for misuse of this software or violations of websites' terms of service.
