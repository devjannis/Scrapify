from dataclasses import dataclass
from typing import List
from discord import Embed

@dataclass
class Variant:
    pid: str
    sku: str
    price: str
    size: str
    quantity: str
    link: str

@dataclass
class Product:
    pid: str
    sku: str
    title: str
    description: str
    link: str
    price: str
    image: str
    vendor: str
    discount: str
    total_reviews: str
    images: List[str]
    variants: List[Variant]
    
    def __str__(self):
        return f"{self.title} by {self.vendor} | {self.description}"
    
    def to_embed(self):
        embed = Embed(
            title=self.title,
            description=self.pid,
            url=self.link
            
        )
        embed.set_thumbnail(url=self.image.src)
        embed.add_field(name="Vendor", value=self.vendor, inline=True)
        embed.add_field(name="Price", value=self.price, inline=True)
        embed.add_field(name="Total Reviews", value=self.total_reviews, inline=True)
        
        pids = " | ".join([v.pid for v in self.variants])
        quantities = " | ".join([v.quantity for v in self.variants])

        embed.add_field(name="Variant PIDs", value=pids or "None", inline=False)
        embed.add_field(name="Quantities", value=quantities or "None", inline=False)

        return embed