from pydantic import BaseModel, EmailStr, field_validator
import re


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    role: str
    salary: float
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        if not re.fullmatch(r"[A-Za-z]+(?:[ -][A-Za-z]+)*", value):
            raise ValueError(
                "Name must contain only letters, spaces, or hyphens"
            )

        return value

    
class EmployeeUpdate(BaseModel):
    name: str
    email: EmailStr
    role: str
    salary: float
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        if not re.fullmatch(r"[A-Za-z]+(?:[ -][A-Za-z]+)*", value):
            raise ValueError(
                "Name must contain only letters, spaces, or hyphens"
            )

        return value


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    salary: float

    class Config:
        from_attributes = True