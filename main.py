from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from controllers.clarifai import router as clarifai_router


app = FastAPI(title="Recipe AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(clarifai_router, prefix="/clarifai", tags=["clarifai"])

handler = Mangum(app)
