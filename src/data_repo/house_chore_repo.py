class HouseChoreRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_all_chores(self, group_id: int):
        self._cursor.execute("SELECT id, name, point, description FROM t_chore WHERE group_id = ?", (group_id,))
        rows = self._cursor.fetchall()
        chores = [{"id": row[0], "name": row[1], "point": row[2], "description": row[3]} for row in rows]
        return chores

    def get_chore_by_id(self, chore_id: int):
        self._cursor.execute("SELECT id, name, point FROM t_chore WHERE id = ?", (chore_id,))
        row = self._cursor.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "point": row[2]}
        return None

    def create_chore(self, name: str, description: str, point: int, group_id: int, ):
        self._cursor.execute(
            "INSERT INTO t_chore (group_id, name, point, description) VALUES (?, ?, ?, ?)",
            (group_id, name, point, description),
        )
        self._conn.commit()
        return self._cursor.lastrowid