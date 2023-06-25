from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    gender: str
    roles: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "rekha",
                "email": "abc@xyz.com",
                "gender": "MALE",
                "roles": "ADMIN"
            }
        }
