class MemberRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_group_members(self, group_id: int):
        self._cursor.execute("SELECT id, member_nickname FROM t_member WHERE group_id = ?", (group_id,))
        rows = self._cursor.fetchall()
        data = [{"id": row[0], "memberNickname": row[1]} for row in rows]
        return data
