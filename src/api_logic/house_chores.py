from src.schemas.pydantic_models.chores import NewChoreModel
from src.settings import logger
from src.services.house_chores import HouseChoreService
from src.common.db_connection import db_context_manager

@db_context_manager
def get_house_chores(conn, **kwargs):
    group_id = kwargs.get("group_id")
    if group_id is None:
        raise ValueError("group_id is required to fetch house chores.")
    data = HouseChoreService(conn).get_chores(group_id=group_id)
    logger.info(f"Fetched user: {data}")
    return {"data": data}

@db_context_manager
def create_house_chore(conn, **kwargs):
    new_chore = NewChoreModel(**kwargs)
    chore_id = HouseChoreService(conn).create_chore(new_chore)
    logger.info(f"Created house chore with ID: {chore_id}")
    return {"choreId": chore_id}
