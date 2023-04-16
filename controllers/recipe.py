from fastapi import APIRouter, UploadFile

import services.clarifai as clarifai_service
import services.edamam as edamam_service
import services.s3 as s3_service
from models.recipe import RecipeResponse

router = APIRouter()


@router.post("/upload_image", response_model=str)
def upload_image(image: UploadFile):
    image_url = s3_service.upload_image(image=image)
    return image_url


@router.get("/infer_ingredient", response_model=str)
def infer_ingredient(image_url: str):
    ingredient = clarifai_service.infer_ingredient(image_url=image_url)
    return ingredient


@router.get("/recipes", response_model=RecipeResponse)
def get_recipes(ingredient: str):
    recipes = edamam_service.search_recipes(ingredient=ingredient)
    return recipes
