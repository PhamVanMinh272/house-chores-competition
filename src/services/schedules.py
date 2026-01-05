from datetime import date, timedelta

from src.common.exceptions import InvalidData
from src.data_repo.member_repo import MemberRepo
from src.data_repo.schedule_repo import ScheduleRepo
from src.data_repo.house_chore_repo import HouseChoreRepo
from src.schemas.pydantic_models.schedules import NewScheduleModel
from src.settings import logger


class ScheduleService:
    def __init__(self, conn):
        self._conn = conn
        self.schedules = None

    def get_schedules(self, group_id: int):
        """
        Get all schedules of a Group (Family).
        :return:
        """
        today = date.today()
        start_date = today - timedelta(days=today.weekday())  # Monday of current week
        end_date = start_date + timedelta(days=6)  # Sunday of current week
        return ScheduleRepo(self._conn).get_all_schedules(group_id=group_id, start_date=str(start_date), end_date=str(end_date))

    def get_schedule(self, schedule_id: int):
        """
        Get a schedule by ID.
        :return:
        """
        return ScheduleRepo(self._conn).get_schedule_by_id(schedule_id)

    def create_schedule(self, new_schedule: NewScheduleModel):
        """

        """

        point = new_schedule.point
        if not new_schedule.point or new_schedule.point == 0:
            # get point from chore
            chore = HouseChoreRepo(self._conn).get_chore_by_id(new_schedule.chore_id)
            if not chore:
                raise InvalidData("Requires point.")
            point = chore["point"]
        schedule_date = new_schedule.schedule_date
        if not new_schedule.schedule_date:
            schedule_date = str(date.today())

        # create chore if chore_id is not provided
        if not new_schedule.chore_id:
            logger.info("Chore ID not provided, creating new chore.")
            group_id = MemberRepo(self._conn).get_member_by_id(new_schedule.member_id)["group"]["id"]
            chore_id = HouseChoreRepo(self._conn).create_chore(new_schedule.new_chore_name, "", point, group_id)
            new_schedule.chore_id = chore_id

        return ScheduleRepo(self._conn).create_schedule(schedule_date, new_schedule.chore_id, new_schedule.member_id, point, new_schedule.status, new_schedule.comment)

    def update_schedule(self, schedule_id: int, member_id:int, schedule_date: str, point: int, status: str, comment: str):
        """
        Update a schedule.
        Get schedule by ID, then update its fields if changed.
        """
        # if (schedule_date: str, status: str, comment: str) is none, keep existing values
        existing_schedule = ScheduleRepo(self._conn).get_schedule_by_id(schedule_id)
        if not existing_schedule:
            raise ValueError(f"Schedule with ID {schedule_id} does not exist.")
        member_id = member_id if member_id is not None else existing_schedule["member"]["id"]
        new_schedule_date = schedule_date if schedule_date is not None else existing_schedule["scheduleDate"]
        new_point = point if point is not None else existing_schedule["point"]
        new_status = status if status is not None else existing_schedule["status"]
        new_comment = comment if comment is not None else existing_schedule["comment"]
        ScheduleRepo(self._conn).update_schedule(schedule_id, member_id, new_schedule_date, new_point, new_status, new_comment)


    def delete_schedule(self, schedule_id: int):
        ScheduleRepo(self._conn).delete_schedule(schedule_id)