from typing import List

from pydantic import BaseModel


class Recipe(BaseModel):
    image: str
    ingredientLines: List[str]
    calories: float
    cuisineType: List[str]
    url: str


class RecipeResponse(BaseModel):
    next_page: str
    recipes: List[Recipe]
