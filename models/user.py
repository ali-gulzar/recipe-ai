from datetime import datetime

from pydantic import BaseModel, EmailStr


class Common(BaseModel):
    name: str
    email: EmailStr


class CreateUser(Common):
    password: str


class User(Common):
    id: str


class LoggedInUser(CreateUser, User):
    pass


class UserToken(BaseModel):
    token_type: str
    access_token: str


class SavedRecipe(BaseModel):
    id: int
    user_id: int
    recipe_id: str
    saved_at: datetime


class SaveUnsaveRecipe(BaseModel):
    recipe_id: str
