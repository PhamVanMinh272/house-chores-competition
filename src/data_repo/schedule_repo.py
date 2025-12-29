# class HouseChoreRepo:
#     def __init__(self, conn):
#         self._conn = conn
#         self._cursor = conn.cursor()
#
#     def get_all_chores(self, group_id: int):
#         self._cursor.execute("SELECT id, name, point FROM t_chore WHERE group_id = ?", (group_id,))
#         rows = self._cursor.fetchall()
#         chores = [{"id": row[0], "name": row[1], "point": row[2]} for row in rows]
#         return chores

class ScheduleRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_all_schedules(self, group_id: int, start_date: str, end_date: str):
            sql = """
            SELECT s.id, s.schedule_date, s.chore_id, c.name, s.member_id, m.member_nickname, c.point, s.status, s.comment
            FROM t_schedule s
            JOIN t_chore c ON s.chore_id = c.id
            JOIN t_member m ON s.member_id = m.id
            WHERE m.group_id = ? AND s.schedule_date BETWEEN ? AND ?
            """
            self._cursor.execute(sql, (group_id, start_date, end_date))
            rows = self._cursor.fetchall()
            schedules = [
                {
                    "id": row[0],
                    "scheduleDate": row[1],
                    "chore": {
                        "id": row[2],
                        "name": row[3],
                    },
                    "member": {
                        "id": row[4],
                        "nickname": row[5],
                    },
                    "point": row[6],
                    "status": row[7],
                    "comment": row[8],
                }
                for row in rows
            ]
            return schedules

    def get_schedule_by_id(self, schedule_id: int):
        sql = """
        SELECT s.id, s.schedule_date, s.chore_id, s.member_id, s.member_nickname, c.point, s.status, s.comment
        FROM t_schedule s
        JOIN t_chore c ON s.chore_id = c.id
        JOIN t_member m ON s.member_id = m.id
        WHERE s.id = ?
        """
        self._cursor.execute(sql, (schedule_id,))
        row = self._cursor.fetchone()
        if row:
            schedule = {
                "id": row[0],
                "scheduleDate": row[1],
                "choreId": row[2],
                "member": {
                    "id": row[3],
                    "nickname": row[4],
                },
                "point": row[5],
                "status": row[6],
                "comment": row[7],
            }
            return schedule
        return None

    def create_schedule(self, schedule_date: str, chore_id: int, member_id: int, point: int, status: str, comment: str):
        sql = """
        INSERT INTO t_schedule (schedule_date, chore_id, member_id, point, status, comment)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self._cursor.execute(sql, (schedule_date, chore_id, member_id, point, status, comment))
        self._conn.commit()
        return self._cursor.lastrowid

    def update_schedule(self, schedule_id: int, schedule_date: str, status: str, comment: str):
        sql = """
        UPDATE t_schedule
        SET schedule_date = ?, status = ?, comment = ?
        WHERE id = ?
        """
        self._cursor.execute(sql, (schedule_date, status, comment, schedule_id))
        self._conn.commit()

    def delete_schedule(self, schedule_id: int):
        sql = "DELETE FROM t_schedule WHERE id = ?"
        self._cursor.execute(sql, (schedule_id,))
        self._conn.commit()