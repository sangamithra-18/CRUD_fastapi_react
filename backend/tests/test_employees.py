import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base

from models import Employee

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

TEST_DATABASE_URL = DATABASE_URL.replace(
    "/employee_db",
    "/employee_test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    db.query(Employee).delete()
    db.commit()

    db.close()
# Create tables in the test database
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)




def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Employee API is running"
    }


def test_create_employee():
    employee = {
        "name": "Test Employee",
        "email": "testemployee@example.com",
        "role": "Developer",
        "salary": 50000
    }

    response = client.post("/employees/", json=employee)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Employee"
    assert data["email"] == "testemployee@example.com"
    assert data["role"] == "Developer"
    assert data["salary"] == 50000
    assert "id" in data


def test_get_employees():
    response = client.get("/employees/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_employee():
    employee = {
        "name": "Get Employee",
        "email": "getemployee@example.com",
        "role": "Developer",
        "salary": 60000
    }

    create_response = client.post("/employees/", json=employee)

    assert create_response.status_code == 201

    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == employee_id
    assert data["name"] == "Get Employee"
    assert data["email"] == "getemployee@example.com"
    assert data["role"] == "Developer"
    assert data["salary"] == 60000


def test_update_employee():
    employee = {
        "name": "Old Name",
        "email": "updateemployee@example.com",
        "role": "Developer",
        "salary": 50000
    }

    # Create employee first
    create_response = client.post("/employees/", json=employee)

    assert create_response.status_code == 201

    employee_id = create_response.json()["id"]

    # Updated data
    updated_employee = {
        "name": "Updated Name",
        "email": "updateemployee@example.com",
        "role": "Senior Developer",
        "salary": 70000
    }

    response = client.put(
        f"/employees/{employee_id}",
        json=updated_employee
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == employee_id
    assert data["name"] == "Updated Name"
    assert data["email"] == "updateemployee@example.com"
    assert data["role"] == "Senior Developer"
    assert data["salary"] == 70000

def test_delete_employee():
    employee = {
        "name": "Delete Employee",
        "email": "deleteemployee@example.com",
        "role": "Tester",
        "salary": 45000
    }

    # Create employee first
    create_response = client.post("/employees/", json=employee)

    assert create_response.status_code == 201

    employee_id = create_response.json()["id"]

    # Delete employee
    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 204


    # Verify employee no longer exists
    get_response = client.get(f"/employees/{employee_id}")

    assert get_response.status_code == 404

def test_get_nonexistent_employee():
    response = client.get("/employees/999999")

    assert response.status_code == 404