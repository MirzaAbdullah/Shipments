from fastapi import FastAPI, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from . import models, schemas, crud
from .database import engine, get_db
from loguru import logger
import sys
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure Loguru
logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

REQUEST_COUNT = Counter("request_count", "Total number of requests", ["method", "endpoint", "http_status"])


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/metrics")
async def get_metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.post("/shipments/", response_model=List[schemas.Shipment], status_code=201)
def create_shipments(shipments: List[schemas.ShipmentCreate], db: Session = Depends(get_db)):
    created_shipments = []
    for shipment in shipments:
        created_shipment = crud.create_shipment(db, shipment)
        created_shipments.append(created_shipment)
    return created_shipments


@app.get("/shipments/", response_model=List[schemas.Shipment])
def read_shipments(
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        carrier: Optional[str] = Query(None),
        min_price: Optional[float] = Query(None),
        max_price: Optional[float] = Query(None),
        db: Session = Depends(get_db)
):
    filters = {}
    if start_date and end_date:
        filters['start_date'] = start_date
        filters['end_date'] = end_date
    if carrier:
        filters['carrier'] = carrier
    if min_price and max_price:
        filters['min_price'] = min_price
        filters['max_price'] = max_price

    shipments = crud.get_shipments(db, filters)
    return shipments
