from dataclasses import dataclass
from typing import Optional, List
from discord import Embed

@dataclass
class QuantityRule:
    min: int # Min cart quantity
    max: Optional[int] # Max cart quantity
    increment: int

@dataclass
class Variant:
    id: int
    title: str
    price: str
    sku: str
    position: int
    barcode: str
    weight: int
    weight_unit: str
    taxable: bool
    requires_shipping: bool
    quantity_rule: QuantityRule
    price_currency: str

@dataclass
class Option:
    id: int
    name: str
    position: int
    values: List[str]
    
@dataclass
class Image: 
    id: int
    position: int
    created_at: str
    updated_at: str
    alt: str
    width: int
    height: int
    src: str
    variant_ids: List[int]

@dataclass
class Product:
    id: int
    title: str
    vendor: str
    product_type: str
    handle: str
    tags: str
    image: Image
    options: List[Option]
    images: List[Image]
    variants: List[Variant]
    
    def __str__(self):
        return f"{self.title} by {self.vendor} ({self.product_type})"
    
    def to_embed(self) -> Embed:
        """
        Converts the product data into a Discord Embed object.

        Returns:
            Embed: A formatted embed containing product details.
        """
        
        embed = Embed(
            title=self.title,
            description=f"🛍️ **{self.product_type}**",
            color=0x3498db 
        )
        
        embed.set_thumbnail(url=self.image.src)
        embed.add_field(name="🏷️ Vendor", value=self.vendor, inline=True)

        if self.tags:
            tag_list = ', '.join(self.tags.split(',')[:15]) 
            embed.add_field(name="🧷 Tags", value=tag_list, inline=False)

        if self.variants:
            first_variant = self.variants[0]
            embed.add_field(
                name="💵 Price",
                value=f"{first_variant.price} {first_variant.price_currency}",
                inline=True
            )

            variant_ids = "\n".join([f"🔹 ID: `{v.id}` | {v.title}" for v in self.variants])
            embed.add_field(name="📦 Variants", value=variant_ids or "None", inline=False)

            quantity_details = "\n".join([
                f"🔢 ID {v.id}: Min `{v.quantity_rule.min}` | Max `{v.quantity_rule.max or 'None'}` | +{v.quantity_rule.increment}"
                for v in self.variants
            ])
            embed.add_field(name="📏 Quantity Rules", value=quantity_details or "None", inline=False)

        return embed
