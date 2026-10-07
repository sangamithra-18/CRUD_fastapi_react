from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import engine, get_db
from models import Base, Employee
from schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)


app = FastAPI(
    title="Employee CRUD API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)



@app.get("/")
def home():
    return {
        "message": "Employee API is running"
    }




@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    try:

        # Check duplicate email
        existing_employee = (
            db.query(Employee)
            .filter(Employee.email == employee.email)
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this email already exists"
            )

        # Create object
        new_employee = Employee(
            name=employee.name,
            email=employee.email,
            role=employee.role,
            salary=employee.salary
        )

        # Add to database
        db.add(new_employee)

        # Save
        db.commit()

        # Get generated ID
        db.refresh(new_employee)

        return new_employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )




@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK
)
def get_employees(
    db: Session = Depends(get_db)
):

    try:

        employees = db.query(Employee).all()

        return employees

    except SQLAlchemyError:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )



@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    try:

        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return employee

    except HTTPException:
        raise

    except SQLAlchemyError:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    try:

        # Find employee
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        # Check if email belongs to another employee
        existing_employee = (
            db.query(Employee)
            .filter(
                Employee.email == employee_data.email,
                Employee.id != employee_id
            )
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another employee already uses this email"
            )

        # Update fields
        employee.name = employee_data.name
        employee.email = employee_data.email
        employee.role = employee_data.role
        employee.salary = employee_data.salary

        # Save changes
        db.commit()

        # Refresh object
        db.refresh(employee)

        return employee

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )



@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    try:

        # Find employee
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        # Delete
        db.delete(employee)

        # Save
        db.commit()

        # 204 means no response body
        return None

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )