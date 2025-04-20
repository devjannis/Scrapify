from dataclasses import dataclass
from typing import List, Optional
from discord_webhook import DiscordEmbed

@dataclass
class GeoLocation:
    latitude: float
    longitude: float
    
@dataclass
class Address:
    street: str
    postal_code: str
    city: str
    country: str
    
@dataclass
class WorkingHours:
    day_of_week: str
    opens: str
    closes: str
    
@dataclass
class Propertys:
    available: bool = False
    flagship: bool = False
    available_for_cc: bool = False
    display_locate_in_store: bool = False
    estimated_delivery_date: Optional[int] = None

@dataclass
class Store:
    name: str
    telephone: str
    identiefer: str
    brand: str
    geo: GeoLocation
    url: str
    address: Address
    image: str
    working_hours: List[WorkingHours]
    propertys: Propertys
    
@dataclass
class Sku:
    sku: str
    name: str
    size: str
    stores: List[Store]
    color: str
    image: str
    
@dataclass
class Product:
    name: str
    sku: str
    product_id: str
    link: str
    skus: List[Sku]
    is_back_order: bool
    sellable_status: bool
    price: str = None
    apple_pay_enabled: bool = False
    
    def __str__(self):
        return f"{self.name} ({self.product_id})"
    
    def to_embed(self) -> DiscordEmbed:
        embed = DiscordEmbed(
            title=self.name,
            description=f"🧾 **SKU:** `{self.sku}`\n🆔 **ID:** `{self.product_id}`",
        )

        embed.add_embed_field(name="💰 Price", value=self.price or "N/A", inline=True)
        embed.add_embed_field(name="📦 Sellable", value=str(self.sellable_status), inline=True)
        embed.add_embed_field(name="⏳ Backorder", value=str(self.is_back_order), inline=True)
        embed.add_embed_field(name="🍏 Apple Pay", value=str(self.apple_pay_enabled), inline=True)

        for sku in self.skus:
            store_list = "\n".join([
                f"🏬 **{store.name}**\n"
                f"✅ Available: {store.propertys.available}, CC: {store.propertys.available_for_cc}"
                for store in sku.stores if store.propertys.available == "true"
            ]) or "No Stores"

            embed.add_embed_field(
                name=f"👟 {sku.name} - {sku.size} ({sku.color})",
                value=store_list,
                inline=False
            )

        if self.skus and self.skus[0].image:
            pass
        
        return embed