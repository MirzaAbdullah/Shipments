from sqlalchemy.orm import Session
from . import models, schemas

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def create_shipment(db: Session, shipment: schemas.ShipmentCreate):
    db_shipment = models.Shipment(
        shipment_number=shipment.shipment_number,
        shipment_date=shipment.shipment_date,
        address_line1=shipment.address.address_line1,
        address_line2=shipment.address.address_line2,
        postal_code=shipment.address.postal_code,
        city=shipment.address.city,
        country_code=shipment.address.country_code,
        length=shipment.length,
        width=shipment.width,
        height=shipment.height,
        weight=shipment.weight,
        price_amount=shipment.price_amount,
        price_currency=shipment.price_currency,
        carrier=shipment.carrier,
    )
    try:
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        return db_shipment.as_dict()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Shipment number already exists")


def get_shipments(db: Session, filters: dict):
    query = db.query(models.Shipment)
    if 'start_date' in filters and 'end_date' in filters:
        query = query.filter(models.Shipment.shipment_date.between(filters['start_date'], filters['end_date']))
    if 'carrier' in filters:
        query = query.filter(models.Shipment.carrier == filters['carrier'])
    if 'min_price' in filters and 'max_price' in filters:
        query = query.filter(models.Shipment.price_amount.between(filters['min_price'], filters['max_price']))
    db_shipments = query.all()

    # Convert SQLAlchemy objects to dictionaries that match the expected Pydantic schema
    return [shipment.as_dict() for shipment in db_shipments]
