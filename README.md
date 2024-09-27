# PARKING MANAGEMENT SYSTEM

This project is a parking management system built using FastAPI. Users can book parking slots, view their bookings, cancel bookings, and provide feedback for their bookings.

## Features

- User authentication and authorization
- Parking slot management
- Booking management (create, view, cancel)
- Feedback management (create, view, delete)
- Relationship management between users, bookings, and feedback

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Pytest

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/virajadigatr/VIRAJ_ADIGA_FASTAPIASSIGNMENT_160924_270924.git
   cd VIRAJ_ADIGA_FASTAPIASSIGNMENT_160924_270924
   
2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt

4. **Set up the database**
5. **Create a .env file in the root directory and add your database configuration**
6. **Running the Application:**

    ```bash
    uvicorn app.main:app --reload
   
7. **Access the application:**

    Open your browser and navigate to http://127.0.0.1:8000.

8. **Testing the Application:**

    ```bash
    pytest app/tests/
   
## API Documentation

FastAPI provides built-in interactive API documentation. You can access it using Swagger UI.

Swagger UI:
Open your browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI.
