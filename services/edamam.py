import os

import requests
from fastapi import status

import models.recipe as recipe_model
from services.ssm_store import get_parameter

EDAMAM_API_URL = os.environ["EDAMAM_API_URL"]
APP_KEY = get_parameter("EDAMAM_APP_KEY")


def search_recipes(ingredient: str) -> recipe_model.RecipeResponse:
    response = requests.get(
        EDAMAM_API_URL,
        params={
            "type": "any",
            "q": ingredient,
            "app_id": "3600a17f",
            "app_key": APP_KEY,
        },
    )

    response.raise_for_status()

    data = response.json()
    recipes = [recipe_model.Recipe.parse_obj(hit["recipe"]) for hit in data["hits"]]

    return recipe_model.RecipeResponse(
        next_page=data.get("_links", {}).get("next", {}).get("href", None),
        recipes=recipes,
    )


def get_recipe(recipe_uri: str) -> recipe_model.Recipe:
    recipe_id = recipe_uri.split("#recipe_")[1]
    response = requests.get(
        f"{EDAMAM_API_URL}/{recipe_id}",
        params={"type": "public", "app_id": "3600a17f", "app_key": APP_KEY},
    )

    response.raise_for_status()

    return recipe_model.Recipe.parse_obj(response.json()["recipe"])
