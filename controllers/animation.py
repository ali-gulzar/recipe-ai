from fastapi import APIRouter
from typing import Dict

import services.s3 as s3_service

router = APIRouter()


@router.get("/{animation_name}", response_model=Dict)
def get_animation(animation_name: str):
    return s3_service.get_animation(animation_name=animation_name)
