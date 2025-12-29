
from src.data_repo.user_repo import UserRepo


class UserService:
    def __init__(self, conn):
        self._conn = conn
        self.users = UserRepo(self._conn).get_all_users()

    def get_users(self):
        """
        Get all users.
        :return:
        """
        return self.users

    def get_groups(self, user_id: int):
        """
        Get groups for a specific user.
        :param user_id:
        :return:
        """
        return UserRepo(self._conn).get_groups(user_id)
