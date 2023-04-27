from typing import Dict

from fastapi import APIRouter

import models.animation as animation_model
import services.s3 as s3_service

router = APIRouter()


@router.get("", response_model=Dict)
def get_animation(animation_name: animation_model.AnimationOptions):
    return s3_service.get_animation(animation_name=animation_name)
