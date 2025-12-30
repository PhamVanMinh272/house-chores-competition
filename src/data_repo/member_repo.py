class MemberRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_group_members(self, group_id: int):
        self._cursor.execute("SELECT id, nickname, hex FROM t_member WHERE group_id = ?", (group_id,))
        rows = self._cursor.fetchall()
        data = [{"id": row[0], "nickname": row[1], "hex": row[2]} for row in rows]
        return data
