from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int
    filename: str
    filepath: str

    class Config:
        from_attributes = True