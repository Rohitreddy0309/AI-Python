from pydantic import BaseModel,EmailStr, constr

class EmployeeBase(BaseModel):
    name: str
    department: str
    project: str
    email: EmailStr
    blood_group: str
    PH_number: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True