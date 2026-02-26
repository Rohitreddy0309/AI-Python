from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsersBase(BaseModel):
    name: str
    email: str
    isActive: bool=True
    createdAt: Optional[datetime] = None
    
class UsersCreate(UsersBase):
    
    pass 

class UsersUpdate(UsersBase):
    pass 
class UserResponse(UsersBase):
    id: int
    class Config:
        from_attributes =True


