import time
import threading

# Initialize task storage and task count
TASKS = {}
count = 1


def add_task():
    global count
    task_name = input("Enter task name: ")
    task_importance = float(input("Enter task importance (1-5): "))
    TASKS[count] = {
        'name': task_name,
        'importance': task_importance,
        'finished_at': None
    }
    count += 1
    print("Task added successfully!\n")


def print_tasks():
    if not TASKS:
        print("No tasks available.\n")
    else:
        for order, details in TASKS.items():
            finished_at = details['finished_at'] if details['finished_at'] else "Not finished"
            print(f"Task {order}: {details['name']} - Importance: {details['importance']} - Finished at: {finished_at}")
        print()


def live_timer(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        elapsed_seconds = int(elapsed_time)
        if elapsed_seconds != 0:
            print(f"\rTime elapsed: {elapsed_seconds} seconds", end="")
        time.sleep(1)
    elapsed_time = time.time() - start_time
    elapsed_seconds = int(elapsed_time) + 1
    print(f"\nTotal time elapsed: {elapsed_seconds} seconds")
    return elapsed_time


def start_task():
    while TASKS:
        task_number = min(TASKS.keys())
        task = TASKS[task_number]

        print(f"\nStarting task {task_number}: {task['name']} - Importance: {task['importance']}")

        start_time = time.time()
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=live_timer, args=(start_time, stop_event))
        timer_thread.start()
        input("\nPress Enter to finish task\n")
        stop_event.set()
        timer_thread.join()

        elapsed_time = time.time() - start_time
        TASKS[task_number]['finished_at'] = elapsed_time
        print(f"\nTask {task_number} finished in {elapsed_time:.2f} seconds.\n")

        del TASKS[task_number]

    print("No more tasks available to start.\n")


def delete_task():
    task_number = int(input("Enter the task number to delete: "))
    if task_number in TASKS:
        del TASKS[task_number]
        print("Task deleted successfully.\n")
    else:
        print("Task not found.\n")


# Main script execution
if __name__ == '__main__':
    print("Welcome to work timer")

    while True:
        print("1. Add task")
        print("2. List tasks")
        print("3. Delete task")
        print("4. Start work")
        print("5. Exit")

        number = int(input("Enter a number: "))

        if number == 1:
            add_task()
        elif number == 2:
            print_tasks()
        elif number == 3:
            delete_task()
        elif number == 4:
            start_task()
        elif number == 5:
            print("Exiting the work timer.")
            break
        else:
            print("Invalid option. Please try again.\n")
