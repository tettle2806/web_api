from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=3, max_length=20)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str