from sqlalchemy import Column, Integer, String, Float
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    role = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)