class MemberRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_group_members(self, group_id: int):
        self._cursor.execute("SELECT id, nickname, hex FROM t_member WHERE group_id = ?", (group_id,))
        rows = self._cursor.fetchall()
        data = [{"id": row[0], "nickname": row[1], "hex": row[2]} for row in rows]
        return data

    def get_member_by_id(self, member_id: int):
        self._cursor.execute("""
        SELECT t_member.id, nickname, hex, group_id, t_group.name
        FROM t_member join t_group on t_member.group_id = t_group.id
        WHERE t_member.id = ?""", (member_id,))
        row = self._cursor.fetchone()
        if row:
            return {"id": row[0], "nickname": row[1], "hex": row[2], "group": {"id": row[3], "name": row[4]}}
        return None
