from pydantic import BaseModel, Field

from random import randint
from enum import Enum


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


def random_destination():
    return randint(110000, 119999)


class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(ge=1, le=25)
    destination: int | None = Field(
        default_factory=random_destination,
        description="Auto-generated ZIP code",
    )
