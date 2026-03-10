from pydantic import BaseModel, Field


class StudentCreateSchema(BaseModel):
    """
    Schema for creating or updating a student
    """

    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0)
    marks: int = Field(..., ge=0)


class StudentResponseSchema(StudentCreateSchema):
    """
    Schema for returning student data.
    """

    id: int

    class config:
        from_attributes = True
