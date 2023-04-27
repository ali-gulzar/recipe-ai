from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from psycopg2.extensions import connection

import services.authentication as authentication_service
import services.database as database_service
from models.user import CreateUser

router = APIRouter()


@router.post("/create")
def create_user(
    user: CreateUser, db: connection = Depends(database_service.connect_db)
):
    data = database_service.create_user(user=user, db=db)
    print(data)
    return "Worked!"


@router.post("/login")
def login_user(request: OAuth2PasswordRequestForm = Depends()):
    # get user from email and verify password using HASH and then create a JWT
    return
