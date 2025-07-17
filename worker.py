import sched
import time
from db_manager import DatabaseManager
from detector_yolo import detect_people


class Consumer:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.currently_running_a_task = False
        self.running_task_id = 0
        check_scheduler = sched.scheduler(time.time, time.sleep)
        check_scheduler.enter(0, 1, self.check_queue, (check_scheduler,))
        check_scheduler.run()

    def check_queue(self, scheduler):
        pending_tasks = self.db_manager.execute_query(
            'SELECT * FROM tasks WHERE status = ? LIMIT 1', ('pending',)
        )

        if self.currently_running_a_task or len(pending_tasks) == 0:
            scheduler.enter(2, 1, self.check_queue, (scheduler,))
            return

        task = pending_tasks[0]
        self.process_task(task)
        scheduler.enter(2, 1, self.check_queue, (scheduler,))

    def process_task(self, task):
        self.currently_running_a_task = True
        self.running_task_id = task[0]

        self.db_manager.execute_query(
            'UPDATE tasks SET status = ? WHERE id = ?',
            ('in_progress', self.running_task_id)
        )

        result = detect_people(task[2], task[4], task[5])

        self.db_manager.execute_query(
            'UPDATE tasks SET result = ? WHERE id = ?',
            (result, self.running_task_id)
        )

        self.end_task()

    def end_task(self):
        self.db_manager.execute_query(
            'UPDATE tasks SET status = ? WHERE id = ?',
            ('done', self.running_task_id)
        )
        self.currently_running_a_task = False


if __name__ == "__main__":
    consumer = Consumer()
