from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from services import ssm_store

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

OAUTH_SECRET_KEY = ssm_store.get_parameter("OAUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
    return payload


def create_access_token(data: dict):
    data_to_encode = data.copy()
    data_to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=30)})

    encoded_jwt = jwt.encode(data_to_encode, OAUTH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
