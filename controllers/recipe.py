from fastapi import APIRouter, Depends, UploadFile

import models.recipe as recipe_model
import services.authentication as authentication_service
import services.clarifai as clarifai_service
import services.edamam as edamam_service
import services.s3 as s3_service

router = APIRouter()


@router.post("/upload_image", response_model=str)
def upload_image(image: UploadFile):
    image_url = s3_service.upload_image(image=image)
    return image_url


@router.get("/infer_ingredient", response_model=str)
def infer_ingredient(image_url: str):
    ingredient = clarifai_service.infer_ingredient(image_url=image_url)
    return ingredient


@router.get("/recipes", response_model=recipe_model.RecipeResponse)
def get_recipes(ingredient: str):
    recipes = edamam_service.search_recipes(ingredient=ingredient)
    return recipes


@router.get(
    "/{recipe_id}",
    response_model=recipe_model.Recipe,
    dependencies=[Depends(authentication_service.get_current_user)],
)
def get_recipe(recipe_id: str):
    return edamam_service.get_recipe(recipe_id=recipe_id)
