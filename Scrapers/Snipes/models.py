from dataclasses import dataclass
from typing import List
from discord import Embed

@dataclass
class Image:
    """Represents an image of the product."""
    id: int
    link: str
    
@dataclass
class Price:
    """Price range of the product."""
    min: str # Minimum price (e.g., for variant)
    max: str # Maximum price
    
@dataclass
class Stock:
    """Represents stock information for a product variant."""
    supplier_id: int # ID of the supplier
    warehouse_id: int # ID of the warehouse
    quantity: int 
    sellable_without_stock: bool # Can be sold even if out of stock
    
@dataclass 
class Variant:
    """Represents a product variant like size or color."""
    pid: int
    stock: Stock
    price: str # Price formatted as string
    size: str # Size label, e.g., '42 EU'
    
@dataclass
class Product:
    """Main product object parsed from the API response."""
    pid: int
    sku: str
    name: str
    price: Price
    uri: str
    release_date_time: str
    active: bool
    new: bool
    sold_out: bool
    masterKey: str
    hot_relase: str
    color: str
    brand: str
    images: List[Image]
    variants: List[Variant]
    
    def __str__(self):
        return f"{self.name} by {self.brand} ({self.sku})"

    def to_embed(self) -> Embed:
        """
        Converts the product data into a Discord Embed object.

        Returns:
            Embed: A formatted embed containing product details.
        """
        
        embed = Embed(
            title=self.name,
            description=f"**{self.brand}** • {self.color}",
            color=0x2ecc71,  
            url=self.uri
        )

        embed.add_field(name="🆔 SKU", value=self.sku, inline=True)
        embed.add_field(
            name="💶 Price", 
            value=f"{self.price.min}€ – {self.price.max}€", 
            inline=True
        )
        embed.add_field(
            name="📅 Release Date", 
            value=f"{self.release_date_time}", 
            inline=False
        )

        embed.add_field(name="✅ Active", value=str(self.active), inline=True)
        embed.add_field(name="🆕 New", value=str(self.new), inline=True)
        embed.add_field(name="❌ Sold Out", value=str(self.sold_out), inline=True)

        embed.set_footer(
            text=f"🔑 Master Key: {self.masterKey} • 🔥 Hot Release: {self.hot_relase}"
        )

        if self.images:
            embed.set_thumbnail(url=self.images[0].link)

        if self.variants:
            variant_lines = [
                f"• Size {v.size}: {v.stock.quantity} in stock" 
                for v in self.variants
            ]
            embed.add_field(
                name="📦 Variants", 
                value="\n".join(variant_lines), 
                inline=False
            )

        return embed
