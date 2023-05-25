from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extensions import connection
from mysql.connector.connection_cext import CMySQLConnection

import models.user as user_model
import services.authentication as authentication_service
import services.database as database_service

router = APIRouter()


@router.post(
    "/create", response_model=user_model.CreatedUser, response_model_exclude_none=True
)
def create_user(
    user: user_model.CreateUser, db: CMySQLConnection = Depends(database_service.connect_db)
):
    return database_service.create_user(user=user, db=db)


@router.post("/login", response_model=user_model.AuthenticatedUser)
def login_user(
    request: OAuth2PasswordRequestForm = Depends(),
    db: CMySQLConnection = Depends(database_service.connect_db),
):
    user: user_model.LoggedInUser = database_service.get_user_by_email(
        request.username, db=db
    )

    if not authentication_service.Hash.verify(request.password, user.password):
        raise HTTPException(
            detail="Incorrect password", status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token = authentication_service.create_access_token(
        data={"email": user.email, "id": user.id, "name": user.name}
    )

    return user_model.AuthenticatedUser(
        name=user.name,
        email=user.email,
        id=user.id,
        token_type="bearer",
        access_token=access_token,
    )


@router.get("/saved-recipes", response_model=List[user_model.SavedRecipe])
def saved_recipes(
    current_user: user_model.User = Depends(authentication_service.get_current_user),
    db: CMySQLConnection = Depends(database_service.connect_db),
):
    return database_service.get_saved_recipes(current_user.id, db=db)


@router.post("/save", response_model=bool)
def save_recipe(
    recipe: user_model.SaveUnsaveRecipe,
    current_user: user_model.User = Depends(authentication_service.get_current_user),
    db: CMySQLConnection = Depends(database_service.connect_db),
):
    database_service.save_recipe(
        user_id=current_user.id, recipe_id=recipe.recipe_id, db=db
    )
    return True


@router.delete("/unsave", response_model=bool)
def unsave_recipe(
    recipe: user_model.SaveUnsaveRecipe,
    current_user: user_model.User = Depends(authentication_service.get_current_user),
    db: CMySQLConnection = Depends(database_service.connect_db),
):
    return database_service.unsave_recipe(
        user_id=current_user.id, recipe_id=recipe.recipe_id, db=db
    )
