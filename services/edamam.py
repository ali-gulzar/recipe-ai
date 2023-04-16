import os

import requests

from models.recipe import Recipe, RecipeResponse
from services.ssm_store import get_parameter

EDAMAM_API_URL = os.environ["EDAMAM_API_URL"]
APP_KEY = get_parameter("EDAMAM_APP_KEY")


def search_recipes(ingredient: str) -> RecipeResponse:
    params = {
        "type": "any",
        "q": ingredient,
        "app_id": "3600a17f",
        "app_key": APP_KEY,
    }
    response = requests.get(EDAMAM_API_URL, params=params)
    data = response.json()
    recipes = [Recipe.parse_obj(hit["recipe"]) for hit in data["hits"]]
    return RecipeResponse(
        next_page=data.get("_links", {}).get("next", {}).get("href", None),
        recipes=recipes,
    )
