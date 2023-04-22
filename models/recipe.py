from typing import List, Optional

from pydantic import BaseModel


class Ingredient(BaseModel):
    text: str
    quantity: float
    measure: Optional[str]
    food: str
    weight: float
    image: Optional[str]


class Recipe(BaseModel):
    label: str
    source: str
    image: str
    ingredientLines: List[str]
    ingredients: List[Ingredient]
    calories: float
    cuisineType: List[str]
    url: str
    totalTime: float


class RecipeResponse(BaseModel):
    next_page: str
    recipes: List[Recipe]
