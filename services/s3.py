import json
import os

import boto3
from fastapi import HTTPException, UploadFile, status

OFFLINE = os.environ.get("OFFLINE") == "true"


def get_s3_client(
    override_offline: str = False,
):
    if OFFLINE and override_offline == False:
        client = boto3.client(
            "s3",
            endpoint_url="http://localhost:4569",
            aws_access_key_id="S3RVER",
            aws_secret_access_key="S3RVER",
        )
    else:
        client = boto3.client("s3")

    return client


def upload_image(
    image: UploadFile,
):
    s3_client = get_s3_client(override_offline=True)
    try:
        s3_client.put_object(
            Bucket="food-images-recipe-ai",
            Key=image.filename,
            Body=image.file.read(),
        )
    except Exception as e:
        raise HTTPException(
            detail=e,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    s3_image_url = f"https://food-images-recipe-ai.s3.amazonaws.com/{image.filename}"
    return s3_image_url


def get_animation(
    animation_name: str,
):
    s3_client = get_s3_client(override_offline=True)
    try:
        response = s3_client.get_object(
            Bucket="recipe-ai-animations",
            Key=f"{animation_name}.json",
        )
        json_data = response["Body"].read().decode("utf-8")

        # Parse the JSON data
        animation_json = json.loads(json_data)
        return animation_json

    except Exception as e:
        raise HTTPException(
            detail=e,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
