from dataclasses import dataclass
from typing import Optional, List
from discord import Embed

@dataclass
class Brand:
    logo: str
    name: str
    pid: str
    show: bool
    url: str

@dataclass
class Product:
    pid: int
    ians: List[str]
    product_type: str
    rating: float
    title: str
    price: int
    discounted: bool
    discount: Optional[int]
    old_price: Optional[int]
    images: List[str]
    brand: Brand
    
    def __str__(self):
        return f"{self.title} by {self.brand.name} ({self.pid})"

    def to_embed(self) -> Embed:
        embed = Embed(
            title=self.title,
            url=self.brand.url,
            description=(
                f"🏷️ **Marke:** {self.brand.name}\n"
                f"🆔 **Produkt-ID:** `{self.pid}`\n"
                f"⭐ **Rating:** {self.rating}/5.0\n"
                f"🛍️ **Typ:** {self.product_type}"
            ),
            color=0x2ecc71
        )

        if self.discounted and self.old_price and self.discount:
            price_text = f"~~{self.old_price}€~~ ➝ **{self.price}€** (-{self.discount}%)"
        else:
            price_text = f"{self.price}€"

        embed.add_field(name="💰 Preis", value=price_text, inline=True)
        embed.add_field(name="🔖 Discounted", value=str(self.discounted), inline=True)

        if self.ians:
            ian_list = "\n".join(f"`{ian}`" for ian in self.ians[:5])
            embed.add_field(name="📦 IANs", value=ian_list, inline=False)

        if self.images:
            embed.set_image(url=self.images[0])
        if self.brand.logo:
            embed.set_thumbnail(url=self.brand.logo)

        embed.set_footer(text=f"Brand PID: {self.brand.pid}")
        return embed
