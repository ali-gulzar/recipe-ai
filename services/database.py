import psycopg2
from fastapi import HTTPException, status
from passlib.context import CryptContext
from psycopg2.extensions import connection

import models.database as database_model
import models.user as user_model
import services.ssm_store as ssm_store_service

DATBASE_PASSWORD = ssm_store_service.get_parameter("DATABASE_PASSWORD")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)

    def verify(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


def connect_db() -> connection:
    try:
        conn = psycopg2.connect(
            dbname="recipe_ai",
            user="recipe_ai",
            password=f"{DATBASE_PASSWORD}",
            host="recipe-ai.clixccayxbxi.eu-west-3.rds.amazonaws.com",
            port="5432",
        )
        return conn
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_424_FAILED_DEPENDENCY
        )


def execute_db(
    db: connection,
    sql_statment: str,
    action: database_model.DATBASE_ACTIONS,
    paramters: tuple = None,
):
    cursor = db.cursor()

    try:
        if paramters:
            cursor.execute(sql_statment, paramters)
        else:
            cursor.execute(sql_statment)

        db.commit()

        if action == database_model.DATBASE_ACTIONS.fetch_all:
            return cursor.fetchall()
        elif action == database_model.DATBASE_ACTIONS.fetch_one:
            return cursor.fetchone()
    except psycopg2.Error as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


def create_user(user: user_model.CreateUser, db: connection) -> user_model.User:
    data = execute_db(
        db=db,
        sql_statment="INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id, email",
        action=database_model.DATBASE_ACTIONS.fetch_one,
        paramters=(user.email, Hash.bcrypt(user.password)),
    )
    id = data[0]
    email = data[1]
    return user_model.User(id=id, email=email)


def get_user_by_email(user_email: str, db: connection) -> user_model.User:
    data = execute_db(
        db=db,
        sql_statment="SELECT * FROM users WHERE email = %s",
        action=database_model.DATBASE_ACTIONS.fetch_one,
        paramters=(user_email,),
    )
    if data:
        id = data[0]
        email = data[1]
        password = data[2]
        return user_model.User(id=id, email=email, password=password)

    raise HTTPException(detail=f"No user with email {user_email} exists!")
