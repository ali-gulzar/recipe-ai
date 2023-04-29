from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Common(BaseModel):
    email: EmailStr


class CreateUser(Common):
    password: str


class User(Common):
    id: Optional[str]
    password: Optional[str]


class LoggedInUser(Common):
    token_type: str
    access_token: str


class SavedRecipe(BaseModel):
    id: int
    user_id: int
    recipe_uri: str
    saved_at: datetime
