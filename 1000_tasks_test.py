from task_scheduler import Scheduler


if __name__ == "__main__":
    scheduler = Scheduler()

    scheduler.clear_done_tasks()

    # Queue 1000 test tasks. Same image but whatever
    for i in range(1000):
        scheduler.insert_task(
            'pending',
            'https://images.fineartamerica.com/images-medium-large-5/busy-streets-of-paris-sheldon-anderson.jpg',
            0
        )
