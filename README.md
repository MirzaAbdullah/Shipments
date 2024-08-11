Shipment API
===================

This project is a FastAPI-based application that manages shipment data, including features like creating, retrieving, and validating shipments. The project also includes performance tests and telemetry features for structured logging and metrics.

Features
--------
- **Shipment Management**: Create and retrieve shipment records with validation.
- **Performance Testing**: Load testing with Locust and benchmarking with pytest-benchmark.
- **Telemetry**: Structured logging with Loguru and metrics with Prometheus.

Getting Started
---------------
### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.11 or later
- `pip` (Python package installer)
- Git (for cloning the repository)

### Installation

Follow these steps to get the project up and running on your local machine:

1. **Clone the repository**:

   Open your terminal and run the following command:
git clone https://github.com/mirzaabdullah/shipment-api.git
cd shipment-api

2. **Create a virtual environment**:

It is recommended to use a virtual environment to isolate your dependencies. Run the following command to create and activate a virtual environment:

#### On macOS/Linux

python3 -m venv venv
source venv/bin/activate


3. **Install the required packages**:

With the virtual environment activated, install the dependencies listed in requirements.txt

`pip install -r requirements.txt`


4. **Set up environment variables**:

Create a `.env` file in the root directory of the project and add the necessary environment variables. For example:

`DATABASE_URL=postgresql://shipment_user:<your-password>@localhost/shipment_db`


5. **Run the application**:

Start the FastAPI application with Uvicorn:

`uvicorn app.main --reload`


The application should now be running at `http://127.0.0.1:8000`.

Running Tests
-------------
This project includes unit tests using `pytest`. Follow these steps to run the tests:

1. **Run unit tests**:

To run all the unit tests, use the following command:


This command will discover and run all tests in the `tests/` directory.

2. **Run performance tests**:

To run performance tests with Locust, follow these steps:

- **Install Locust** (if not already installed):

  ```
  pip install locust
  ```

- **Run Locust**:

  ```
  locust -f locustfile.py
  ```

- Open your browser and navigate to `http://localhost:8089` to configure and start the load test.

Telemetry
---------
The project includes telemetry with structured logging and Prometheus metrics:

- **Logging**: Logs are output to the console using Loguru.
- **Metrics**: Prometheus metrics can be accessed at `http://127.0.0.1:8000/metrics`.


- **app/**: Contains the main application code.
  - `main.py`: Entry point for the FastAPI application.
  - `models.py`: SQLAlchemy models for the database.
  - `schemas.py`: Pydantic models for request and response validation.
  - `crud.py`: CRUD operations for interacting with the database.
  - `database.py`: Database connection and session management.

- **tests/**: Contains unit tests for the application.
- **requirements.txt**: Python dependencies.


Swagger API
-------
This project has swagger api integrated which can be viewed at `http://127.0.0.1:8000/docs#/`

---
Thank you for your interest in the Shipment API project! If you encounter any issues or have questions, please don't hesitate to reach out.









