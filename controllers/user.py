from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extensions import connection

import models.user as user_model
import services.authentication as authentication_service
import services.database as database_service

router = APIRouter()


@router.post(
    "/create", response_model=user_model.User, response_model_exclude_none=True
)
def create_user(
    user: user_model.CreateUser, db: connection = Depends(database_service.connect_db)
):
    return database_service.create_user(user=user, db=db)


@router.post("/login", response_model=user_model.LoggedInUser)
def login_user(
    request: OAuth2PasswordRequestForm = Depends(),
    db: connection = Depends(database_service.connect_db),
):
    user: user_model.User = database_service.get_user_by_email(request.username, db=db)

    if not authentication_service.Hash.verify(request.password, user.password):
        raise HTTPException(
            detail="Incorrect password", status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token = authentication_service.create_access_token(
        data={"email": user.email, "id": user.id}
    )

    return user_model.LoggedInUser(
        email=user.email, token_type="bearer", access_token=access_token
    )


@router.get("/saved-recipes", response_model=List[user_model.SavedRecipe])
def saved_recipes(
    current_user: user_model.User = Depends(authentication_service.get_current_user),
    db: connection = Depends(database_service.connect_db),
):
    return database_service.get_saved_recipes(current_user.id, db=db)


@router.post("/save/{recipe_uri}", response_model=user_model.SavedRecipe)
def save_recipe(
    recipe_uri: str,
    current_user: user_model.User = Depends(authentication_service.get_current_user),
    db: connection = Depends(database_service.connect_db),
):
    return database_service.save_recipe(
        user_id=current_user.id, recipe_uri=recipe_uri, db=db
    )
