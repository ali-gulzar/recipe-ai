from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

import models.user as user_model
import services.ssm_store as ssm_store_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

OAUTH_SECRET_KEY = ssm_store_service.get_parameter("OAUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, OAUTH_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    # get user details from database using the payload
    if payload is None:
        raise credentials_exception
    return user_model.User(id=payload["id"], email=payload["email"])


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, OAUTH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
