import secrets
from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from users.crud import get_user_by_username



