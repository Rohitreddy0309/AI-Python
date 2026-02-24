from sqlalchemy import Column, Integer, String, Enum
from core.db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    department = Column(Enum('Python','Java','C#','Network','Security', name="department_enum"))
    project = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    blood_group = Column(Enum('A+','A-','B+','B-','AB+','AB-','O+','O-', name="blood_group_enum"))
    PH_number = Column(String, unique=True, nullable=False)
