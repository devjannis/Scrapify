from dataclasses import dataclass
from typing import List
import pytz
from datetime import datetime
from discord import Embed

@dataclass 
class Variant:
    pid: str
    group: str
    gtin: str
    size: str
    
@dataclass
class AvailabilityVariant:
    pid: str
    available: bool
    level: str

@dataclass
class Product:
    name: str
    sku: str
    price: float
    discounted: bool
    currency: str
    channels: List[str]
    genders: List[str]
    quantity_limit: int
    publish_type: str
    exclusive_access: bool
    commerce_start_date: str
    availability_variants: List[AvailabilityVariant]
    variants: List[Variant]
    
    def __str__(self):
        return f"{self.name} for {self.price} {self.currency} ({self.sku})"
    
    def to_embed(self) -> Embed:
        """
        Converts the product data into a Discord Embed object.

        Returns:
            Embed: A formatted embed containing product details.
        """
        
        embed = Embed(
            title=self.name,
            description=f"```{self.sku}```",
        )
        try:
            dt = datetime.fromisoformat(self.commerce_start_date.replace("Z", "+00:00"))
            dt = dt.replace(tzinfo=None)
            german_tz = pytz.timezone("Europe/Berlin")
            dt_german = pytz.utc.localize(dt).astimezone(german_tz)
            unix_timestamp = int(dt_german.timestamp())
            embed.add_field(name="Release Date", value=f"<t:{unix_timestamp}:f>", inline=False)
        except:
            embed.add_field(name="Release Date", value="N/A", inline=False)

        embed.add_field(name="SKU", value=self.sku, inline=True)
        embed.add_field(name="Price", value=f"{self.price} {self.currency}", inline=True)
        embed.add_field(name="Discounted", value=f"{self.discounted}", inline=True)
        embed.add_field(name="Exclusive Access", value=str(self.exclusive_access), inline=True)
        embed.add_field(name="Publish Type", value=self.publish_type, inline=True)
        embed.add_field(name="Quantity Limit", value=str(self.quantity_limit), inline=True)

        sizes = [v.size for v in self.variants]
        levels = [av.level for av in self.availability_variants]

        if sizes:
            embed.add_field(name="Sizes", value="```" + "\n".join(sizes) + "```", inline=True)
        else:
            embed.add_field(name="Sizes", value="```N/A```", inline=True)

        if levels:
            embed.add_field(name="Stock", value="```" + "\n".join(levels) + "```", inline=True)
        else:
            embed.add_field(name="Stock", value="```N/A```", inline=True)        

        embed.set_thumbnail(url=f"https://secure-images.nike.com/is/image/DotCom/{self.sku.replace('-', '_')}_A_PREM?width=820&height=820")

        return embed