from src.data_repo.house_chore_repo import HouseChoreRepo
from src.schemas.pydantic_models.chores import NewChoreModel


class HouseChoreService:
    def __init__(self, conn):
        self._conn = conn
        self.chores = None

    def get_chores(self, group_id: int):
        """
        Get all house chores of a Group (Family).
        :return:
        """
        return HouseChoreRepo(self._conn).get_all_chores(group_id=group_id)

    def create_chore(self, new_chore: NewChoreModel):
        """
        Create a new house chore.
        :return:
        """
        return HouseChoreRepo(self._conn).create_chore(new_chore.name, new_chore.description, new_chore.point, new_chore.group_id)