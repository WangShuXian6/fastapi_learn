from pydantic import BaseModel, Field

from random import randint


def random_destination():
    return randint(110000, 119999)


class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(ge=1, le=25)
    destination: int | None = Field(
        default_factory=random_destination,
        description="Auto-generated ZIP code",
    )
