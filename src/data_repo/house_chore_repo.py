class HouseChoreRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_all_chores(self, group_id: int):
        self._cursor.execute("SELECT id, name, point FROM t_chore WHERE group_id = ?", (group_id,))
        rows = self._cursor.fetchall()
        chores = [{"id": row[0], "name": row[1], "point": row[2]} for row in rows]
        return chores

    def get_chore_by_id(self, chore_id: int):
        self._cursor.execute("SELECT id, name, point FROM t_chore WHERE id = ?", (chore_id,))
        row = self._cursor.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "point": row[2]}
        return None