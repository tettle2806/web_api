from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError
from pydantic import EmailStr
from core import config

from core.config import pwd_context
from core.models import db_helper


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# class UserAuth:
#
#     async def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
#         to_encode = data.copy()
#         expire = datetime.now(timezone.utc) + expires_delta
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(
#             to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
#         )
#         return encoded_jwt
#
#     async def decode_token(self, token: str):
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
#         return payload
#
#     async def login_for_access_token(self, email: str, password: str) -> Token:
#         user: UserDTO = self.validate_user(email=email, password=password)
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = self.create_access_token(
#             data={"email": user.email, "password": user.password},
#             expires_delta=access_token_expires,
#         )
#         return Token(
#             access_token=access_token,
#             token_type="bearer",
#             access_token_expires=access_token_expires,
#         )
#
#     async def validate_user(
#         self, email: EmailStr, password: str
#     ) -> Union[UserDTO, bool]:
#         hashed = await hash_password(password)
#         async with db_helper.session_factory() as session:
#             user: UserDTO = await get_user_by_username(session=session, email=email)
#         if user and user.password.__eq__(hashed):
#             print(user)
#             return user
#         return False
#
#     async def get_current_user(self, token: str):
#         credentials_exeptions = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#         try:
#             payload = jwt.decode(
#                 token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
#             )
#
#             email: str = payload.get("email")
#             password: str = payload.get("password")
#             exp: str = payload.get("exp")
#
#             if email is None:
#                 raise credentials_exeptions
#
#         except InvalidTokenError:
#             raise credentials_exeptions
#
#         user: UserDTO = await self.validate_user(email=email, password=password)
#
#         if user is None:
#             raise credentials_exeptions
#         return user
