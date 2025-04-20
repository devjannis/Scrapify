from dataclasses import dataclass
from typing import List
from discord import Embed

@dataclass
class Price:
    value: str
    
@dataclass
class Stock:
    quantity: str

@dataclass
class Offer:
    price: Price 
    stock: Stock

@dataclass
class Variant:
    size: str
    sku: str
    supplierSize: str
    offer: Offer
    
@dataclass 
class Brand:
    name: str
    id: str
    
@dataclass
class Color:
    name: str

@dataclass
class Image:
    uri: str
    
@dataclass
class DeliveryOption:
    label: str
    description: str
    feeLabel: str
    kind: str
    

@dataclass
class Product:
    sku: str
    name: str
    uri: str
    group: str
    comingSoon: bool
    isActive: bool
    brand: Brand
    color: Color
    price: Price
    variants: List[Variant]
    images: List[Image]
    
    def __str__(self):
        return f"{self.name} by {self.brand.name} ({self.group})"

    def to_embed(self) -> Embed:
        """
        Converts the product data into a Discord Embed object.

        Returns:
            Embed: A formatted embed containing product details.
        """
        embed = Embed(
            title=self.name,
            url=self.uri,
            description=(
                f"🧾 **SKU:** `{self.sku}`\n"
                f"🏷️ **Brand:** {self.brand.name}\n"
                f"🎨 **Color:** {self.color.name}"
            ),
        )
        embed.add_field(name="📦 Group", value=self.group, inline=True)
        embed.add_field(name="💰 Price", value=f"{self.price.value} €", inline=True)
        embed.add_field(name="✅ Active", value=str(self.isActive), inline=True)
        embed.add_field(name="⏳ Coming Soon", value=str(self.comingSoon), inline=True)

        if self.variants:
            variant_text = "\n".join(
                f"🔹 `{v.size}` ({v.sku}) — {v.offer.price.value} € | {v.offer.stock.quantity}x"
                for v in self.variants
            )
        else:
            variant_text = "None"

        embed.add_field(name="🧵 Variants", value=variant_text, inline=False)

        if self.images:
            embed.set_image(url=self.images[0].uri)

        embed.set_footer(text=f"🆔 Brand ID: {self.brand.id}")
        return embed