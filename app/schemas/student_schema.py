from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    marks: int


class StudentUpdate(BaseModel):
    name: str
    age: int
    marks: int


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    marks: int

    class Config:
        from_attributes = True