from src.settings import logger
from src.services.users import UserService
from src.common.db_connection import db_context_manager

@db_context_manager
def get_users(conn, **kwargs):
    data = UserService(conn).get_users()
    logger.info(f"Fetched user: {data}")
    return {"data": data}


@db_context_manager
def create_user(conn, user_data, **kwargs):
    user_id = UserService(conn).create_user(user_data)
    logger.info(f"Created user with ID: {user_id}")
    return {"userId": user_id}

@db_context_manager
def get_groups(conn, **kwargs):
    user_id = kwargs.get("user_id")
    data = UserService(conn).get_groups(user_id)
    logger.info(f"Fetched groups: {data}")
    return {"data": data}
