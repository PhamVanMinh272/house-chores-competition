from src.schemas.pydantic_models.schedules import NewScheduleModel
from src.settings import logger
from src.services.schedules import ScheduleService
from src.common.db_connection import db_context_manager

@db_context_manager
def get_schedules(conn, **kwargs):
    group_id = kwargs.get("group_id")
    if group_id is None:
        raise ValueError("group_id is required to fetch schedules.")
    data = ScheduleService(conn).get_schedules(group_id=group_id)
    logger.info(f"Fetched data: {data}")
    return {"data": data}

@db_context_manager
def get_schedule(conn, schedule_id, **kwargs):
    data = ScheduleService(conn).get_schedule(schedule_id)
    logger.info(f"Fetched schedule: {data}")
    return {"data": data}

@db_context_manager
def create_schedule(conn, **kwargs):
    print(kwargs)
    schedule_schema = NewScheduleModel(**kwargs)
    schedule_data = schedule_schema.model_dump()
    schedule_id = ScheduleService(conn).create_schedule(**schedule_data)
    logger.info(f"Created schedule with ID: {schedule_id}")
    return {"schedule_id": schedule_id}


@db_context_manager
def update_schedule(conn, schedule_id, **kwargs):
    logger.info(f"Updating schedule ID {schedule_id} with data: {kwargs}")
    schedule_schema = NewScheduleModel(**kwargs)
    schedule_data = schedule_schema.model_dump(by_alias=False, exclude={"chore_id"})
    ScheduleService(conn).update_schedule(schedule_id, **schedule_data)
    logger.info(f"Updated schedule with ID: {schedule_id}")
    return {"status": "success"}


@db_context_manager
def delete_schedule(conn, schedule_id, **kwargs):
    ScheduleService(conn).delete_schedule(schedule_id)
    logger.info(f"Deleted schedule with ID: {schedule_id}")
    return {"status": "success"}