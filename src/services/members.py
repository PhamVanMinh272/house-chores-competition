from src.data_repo.member_repo import MemberRepo


class MemberService:
    def __init__(self, conn):
        self._conn = conn
        self.members = None

    def get_members(self, group_id: int):
        """
        Get all members.
        :return:
        """
        return MemberRepo(self._conn).get_group_members(group_id)
