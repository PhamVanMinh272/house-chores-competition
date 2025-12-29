class UserRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_all_users(self):
        self._cursor.execute("SELECT id, name FROM t_user")
        rows = self._cursor.fetchall()
        data = [{"id": row[0], "name": row[1]} for row in rows]
        return data

    def get_groups(self, user_id: int):
        """
        select t_group.id, t_group.name
        from t_group
        join t_member on t_group.id = t_member.group_id
        where t_member.user_id = <user_id>
        """
        self._cursor.execute(
            """
            SELECT t_group.id, t_group.name
            FROM t_group
            JOIN t_member ON t_group.id = t_member.group_id
            WHERE t_member.user_id = ?
            """,
            (user_id,),
        )
        rows = self._cursor.fetchall()
        groups = [{"id": row[0], "name": row[1]} for row in rows]
        return groups
