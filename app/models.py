from sqlalchemy import Column, Integer, String, Date, Float
from .database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String, unique=True, index=True, nullable=False)
    shipment_date = Column(Date, nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    price_amount = Column(Float, nullable=False)
    price_currency = Column(String, nullable=False)
    carrier = Column(String, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "shipment_number": self.shipment_number,
            "shipment_date": self.shipment_date,
            "address": {
                "address_line1": self.address_line1,
                "address_line2": self.address_line2,
                "postal_code": self.postal_code,
                "city": self.city,
                "country_code": self.country_code,
            },
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "weight": self.weight,
            "price_amount": self.price_amount,
            "price_currency": self.price_currency,
            "carrier": self.carrier,
        }
