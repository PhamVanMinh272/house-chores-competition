from src.data_repo.house_chore_repo import HouseChoreRepo

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