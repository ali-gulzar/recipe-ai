from typing import List

from fastapi import HTTPException, status

import models.database as database_model
import models.user as user_model
import services.authentication as authentication_service
import services.ssm_store as ssm_store_service
from mysql.connector import connect, Error
from mysql.connector.connection_cext import CMySQLConnection

DATBASE_PASSWORD = ssm_store_service.get_parameter("DATABASE_PASSWORD")

DATABASE_CONFIG = {
    'user': "c8hlks8r77kan6pdoa8x",
    'passwd': DATBASE_PASSWORD,
    'db': 'recipe-ai',
    'host': 'aws.connect.psdb.cloud'
}

def connect_db() -> CMySQLConnection:
    try:
        conn = connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_424_FAILED_DEPENDENCY
        )


def execute_db(
    db: CMySQLConnection,
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

        if action == database_model.DATBASE_ACTIONS.insert:
            db.commit()
            return
        elif action == database_model.DATBASE_ACTIONS.delete:
            db.commit()
            return cursor.rowcount > 0
        elif action == database_model.DATBASE_ACTIONS.fetch_one:
            return cursor.fetchone()
        elif action == database_model.DATBASE_ACTIONS.fetch_all:
            return cursor.fetchall()

    except Error as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


def create_user(user: user_model.CreateUser, db: CMySQLConnection) -> user_model.CreatedUser:
    execute_db(
        db=db,
        sql_statment="INSERT INTO users (email, password, name) VALUES (%s, %s, %s)",
        action=database_model.DATBASE_ACTIONS.insert,
        paramters=(
            user.email,
            authentication_service.Hash.bcrypt(user.password),
            user.name,
        ),
    )
    return user_model.CreatedUser(email=user.email, name=user.name)


def get_user_by_email(user_email: str, db: CMySQLConnection) -> user_model.LoggedInUser:
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
        name = data[3]
        return user_model.LoggedInUser(id=id, email=email, password=password, name=name)

    raise HTTPException(detail=f"No user with email {user_email} exists!", status_code=status.HTTP_404_NOT_FOUND)


def save_recipe(user_id: int, recipe_id: str, db: CMySQLConnection):
    execute_db(
        db=db,
        sql_statment="INSERT INTO saved_recipes (user_id, recipe_id) VALUES (%s, %s)",
        action=database_model.DATBASE_ACTIONS.insert,
        paramters=(user_id, recipe_id),
    )


def unsave_recipe(user_id: int, recipe_id: str, db: CMySQLConnection) -> bool:
    response = execute_db(
        db=db,
        sql_statment="DELETE FROM saved_recipes WHERE user_id = %s and recipe_id = %s",
        action=database_model.DATBASE_ACTIONS.delete,
        paramters=(user_id, recipe_id),
    )
    return response


def get_saved_recipes(user_id: int, db: CMySQLConnection) -> List[user_model.SavedRecipe]:
    data = execute_db(
        db=db,
        sql_statment="SELECT * FROM saved_recipes WHERE user_id = %s",
        action=database_model.DATBASE_ACTIONS.fetch_all,
        paramters=(user_id,),
    )
    return [
        user_model.SavedRecipe(
            user_id=saved_recipe[0],
            recipe_id=saved_recipe[1],
            saved_at=saved_recipe[2],
        )
        for saved_recipe in data
    ]
