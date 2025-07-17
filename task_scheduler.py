from db_manager import DatabaseManager


class Scheduler:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.execute_query('''
         CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             status TEXT,
             path_or_url TEXT NOT NULL,
             result INTEGER,
             save INTEGER,
             save_path TEXT
         )
         ''')

    def insert_task(self, status, path_or_url, result, return_id=False,
                    save_processed_img=False,
                    save_to_path=''):
        self.db_manager.execute_query(
            '''INSERT INTO tasks (status, path_or_url, result, save, save_path)
            VALUES (?, ?, ?, ?, ?)''',
            (status, path_or_url, result, int(save_processed_img), save_to_path)
        )

        if return_id:
            task_id = self.db_manager.execute_query(
                "SELECT id FROM tasks ORDER BY id DESC LIMIT 1"
            )
            return {"task_id": task_id[0][0]} if task_id else None

    def clear_done_tasks(self):
        self.db_manager.execute_query(
            'DELETE FROM tasks WHERE status = ?',
            ('done',)
        )

    # For tests only
    def clear_queue(self):
        self.db_manager.execute_query(
            'DELETE FROM tasks'
        )

    def task_status_by_id(self, task_id):
        query = """
            SELECT status,
               CASE WHEN status = 'done' THEN result ELSE NULL END AS result
            FROM tasks
            WHERE id = ?
        """
        row = self.db_manager.execute_query(query, (task_id,))

        if row:
            status, result = row[0]
            return {"status": status, "result": result} \
                if status == "done" else {"status": status}
        else:
            return {"error": f"Could not find task with id: {task_id}"}

    def check_status(self):
        query = """
            SELECT status, COUNT(*)
            FROM tasks
            WHERE status IN ('pending', 'in_progress', 'done')
            GROUP BY status
        """
        counts = self.db_manager.execute_query(query)

        result = {status: count for status, count in counts}
        total = sum(result.values())
        result.update({"total": total})

        return result
