from dataclasses import dataclass
from typing import List
from discord import Embed

@dataclass
class Category:
    name: str
    key: str
    url: str

@dataclass
class Brand:
    name: str
    logo: str
    
@dataclass
class Image:
    url: str

@dataclass
class Product:
    pid: str
    name: str
    slug: str
    description: str
    next_stock_drop_date: str
    color: str
    categorys: List[Category]
    price: str
    sale_percentage: int
    images: List[Image]
    brand: Brand
    
    def __str__(self):
        return f"{self.name} by {self.brand.name} ({self.pid})"
    
    def to_embed(self) -> Embed:
        embed = Embed(
            title=self.name,
            url=f"https://www.lego.com/en-de/product/{self.slug}",
            description=(
                f"📝 **Description:** {self.description or 'No description available'}\n"
                f"🎨 **Color:** {self.color}\n"
                f"📦 **Next Stock Drop:** {self.next_stock_drop_date or 'Unknown'}"
            ),
            color=0x1abc9c
        )

        embed.add_field(name="💰 Price", value=self.price, inline=True)
        embed.add_field(name="📉 Sale", value=f"-{self.sale_percentage}%", inline=True)

        if self.categorys:
            cat_list = ", ".join([cat.name for cat in self.categorys[:5]])
            embed.add_field(name="🗂️ Categories", value=cat_list, inline=False)

        if self.images:
            embed.set_image(url=self.images[0].url)
        if self.brand.logo:
            embed.set_thumbnail(url=self.brand.logo)

        embed.set_footer(text=f"Brand: {self.brand.name} | PID: {self.pid}")
        return embed
