import os
import boto3
from fastapi import UploadFile, HTTPException, status

OFFLINE = os.environ["OFFLINE"] == "true"


def get_s3_client(override_offline: str = False):
    if OFFLINE and override_offline == False:
        client = boto3.client(
            "s3",
            endpoint_url='http://localhost:4569',
            aws_access_key_id='S3RVER',
            aws_secret_access_key='S3RVER'
        )
    else:
        client = boto3.client("s3")

    return client


def upload_image(image: UploadFile):
    s3_client =  get_s3_client(override_offline=True)
    try:
        s3_client.put_object(Bucket='food-images-recipe-ai', Key=image.filename, Body=image.file.read())
    except Exception as e:
        raise HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)

    s3_image_url = f'https://food-images-recipe-ai.s3.amazonaws.com/{image.filename}'
    return s3_image_url
