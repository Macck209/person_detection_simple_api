import sqlite3


class DatabaseManager:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(DatabaseManager, cls).__new__(cls)
            cls.instance.conn = sqlite3.connect(
                'queue.db',
                check_same_thread=False
            )
            cls.instance.cursor = cls.instance.conn.cursor()
        return cls.instance

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def show_last_tasks(self):
        res = self.cursor.execute(
            "SELECT * FROM tasks ORDER BY id DESC LIMIT 10"
        )
        for tup in reversed(res.fetchall()):
            print(tup)

    def close_connection(self):
        self.conn.close()
