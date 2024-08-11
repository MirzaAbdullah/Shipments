# tests/test_main.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set up an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create the database tables
Base.metadata.create_all(bind=engine)


# Testing the GET /shipments/ Endpoint
@pytest.mark.asyncio
async def test_get_shipments():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/shipments/")
    assert response.status_code == 200
    assert response.json() == []  # Initially, it should return an empty list


# Testing the POST /shipments/ Endpoint
@pytest.mark.asyncio
async def test_post_shipments():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = [
            {
                "shipment_number": "1234567895",
                "shipment_date": "2024-08-12",
                "address": {
                    "address_line1": "456 Test Avenue",
                    "address_line2": "",
                    "postal_code": "54321",
                    "city": "Testtown",
                    "country_code": "US"
                },
                "length": 40,
                "width": 25,
                "height": 15,
                "weight": 800,
                "price_amount": 19.99,
                "price_currency": "USD",
                "carrier": "ups"
            }
        ]
        response = await ac.post("/shipments/", json=payload)
    assert response.status_code == 201
    assert response.json()[0]["shipment_number"] == "1234567895"


# Testing Validation and Error Handling
@pytest.mark.asyncio
async def test_post_shipment_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = [
            {
                "shipment_number": "invalid shipment",  # Invalid shipment number (not alphanumeric)
                "shipment_date": "2024-08-12",
                "address": {
                    "address_line1": "456 Test Avenue",
                    "address_line2": "",
                    "postal_code": "54321",
                    "city": "Testtown",
                    "country_code": "US"
                },
                "length": 40,
                "width": 25,
                "height": 15,
                "weight": 800,
                "price_amount": 19.99,
                "price_currency": "USD",
                "carrier": "ups"
            }
        ]
        response = await ac.post("/shipments/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
