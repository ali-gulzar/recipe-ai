from fastapi import APIRouter, UploadFile, File

import services.clarifai as clarifai_service
import models.clarifai as clarifai_model
import services.s3 as s3_service

router = APIRouter()


@router.post("/upload_image")
def upload_image(image: UploadFile):
    image_url = s3_service.upload_image(image=image)
    return image_url

@router.post("/infer_ingredient")
def infer_ingredient(image: clarifai_model.Image):
    ingredient = clarifai_service.infer_ingredient(image=image)
    return ingredient