from pydantic import BaseModel, Field, field_validator, conint, condecimal
from datetime import date
from typing import Optional

class Address(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    postal_code: str
    city: str
    country_code: str = Field(..., min_length=2, max_length=2)

class ShipmentBase(BaseModel):
    shipment_number: str = Field(..., min_length=1)
    shipment_date: date
    address: Address
    length: conint(gt=0)
    width: conint(gt=0)
    height: conint(gt=0)
    weight: conint(gt=0)
    price_amount: condecimal(gt=0, decimal_places=2)
    price_currency: str = Field(..., min_length=3, max_length=3)
    carrier: str = Field(..., pattern="^(dhl-express|ups|fedex)$")

    # Use `@field_validator` for custom validation logic
    @field_validator("shipment_number")
    @classmethod
    def validate_shipment_number(cls, v):
        if not v.isalnum():
            raise ValueError("Shipment number must be alphanumeric")
        return v

    @field_validator("price_currency")
    @classmethod
    def validate_currency(cls, v):
        valid_currencies = ["USD", "EUR", "GBP"]
        if v not in valid_currencies:
            raise ValueError("Invalid currency code")
        return v

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int

    class Config:
        orm_mode = True
