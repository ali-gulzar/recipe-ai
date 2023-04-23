from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from controllers.animation import router as animation_router
from controllers.recipe import router as recipe_router

app = FastAPI(title="Recipe AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(recipe_router, prefix="/recipe", tags=["recipe"])
app.include_router(animation_router, prefix="/animation", tags=["animation"])

handler = Mangum(app)
