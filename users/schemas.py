from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class UserPD(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDTO(UserPD):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str
