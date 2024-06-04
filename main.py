import time
import threading
import curses

# Initialize task storage and task count
TASKS = {}
count = 1


def center_text(screen, text, y_offset=0):
    height, width = screen.getmaxyx()
    x = width // 2 - len(text) // 2
    y = height // 2 + y_offset
    screen.addstr(y, x, text)


def add_task(screen):
    global count
    screen.clear()
    center_text(screen, "Enter task name: ")
    screen.refresh()
    curses.echo()
    task_name = screen.getstr().decode("utf-8")
    screen.clear()
    center_text(screen, "Enter task importance (1-5): ")
    screen.refresh()
    task_importance = float(screen.getstr().decode("utf-8"))
    TASKS[count] = {
        'name': task_name,
        'importance': task_importance,
        'finished_at': None,
        'completed': False
    }
    count += 1
    screen.clear()
    center_text(screen, "Task added successfully!\nPress any key to continue...")
    screen.refresh()
    screen.getch()
    curses.noecho()


def print_tasks(screen, y_offset=0):
    if not TASKS:
        center_text(screen, "No tasks available.\n", y_offset)
    else:
        for order, details in TASKS.items():
            finished_at = details['finished_at'] if details['finished_at'] else "Not finished"
            completed = "Completed" if details['completed'] else "In progress"
            task_info = f"Task {order}: {details['name']} - Importance: {details['importance']} - Finished at: {finished_at} - {completed}"
            center_text(screen, task_info, y_offset)
            y_offset += 2  # Increase line spacing


def live_timer(start_time, stop_event, screen, y_offset, total_elapsed):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        elapsed_seconds = int(elapsed_time) + 1  # Start at 1 second
        screen.clear()
        print_tasks(screen, y_offset - 4 * len(TASKS))  # Adjust y_offset to list tasks above the timer
        center_text(screen, f"Time elapsed for this task: {elapsed_seconds} seconds", y_offset)
        total_time = total_elapsed + elapsed_seconds
        center_text(screen, f"Total time elapsed: {total_time} seconds", y_offset + 2)
        screen.refresh()
        time.sleep(1)
    elapsed_time = time.time() - start_time
    elapsed_seconds = int(elapsed_time) + 1
    total_time = total_elapsed + elapsed_seconds
    screen.clear()
    center_text(screen, f"Total time elapsed: {total_time} seconds", y_offset + 2)
    screen.refresh()
    return elapsed_time


def start_task(screen):
    total_elapsed = sum(task['finished_at'] for task in TASKS.values() if task['finished_at'])
    while any(not task['completed'] for task in TASKS.values()):
        task_number = min(order for order, task in TASKS.items() if not task['completed'])
        task = TASKS[task_number]

        screen.clear()
        y_offset = -4 * len(TASKS) // 2
        print_tasks(screen, y_offset)
        y_offset += 4 * len(TASKS)  # Adjust y_offset after listing tasks
        center_text(screen, f"Starting task {task_number}: {task['name']} - Importance: {task['importance']}\n",
                    y_offset)
        screen.refresh()

        start_time = time.time()
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=live_timer,
                                        args=(start_time, stop_event, screen, y_offset + 2, total_elapsed))
        timer_thread.start()

        curses.echo()
        center_text(screen, "\nPress Enter when you finish the task...", y_offset + 6)
        screen.refresh()
        screen.getstr()

        stop_event.set()
        timer_thread.join()

        elapsed_time = time.time() - start_time
        TASKS[task_number]['finished_at'] = elapsed_time
        TASKS[task_number]['completed'] = True
        total_elapsed += elapsed_time
        screen.clear()
        center_text(screen,
                    f"\nTask {task_number} finished in {elapsed_time:.2f} seconds.\nPress any key to continue...")
        screen.refresh()
        screen.getch()
        curses.noecho()

    screen.clear()
    center_text(screen, "All tasks have been completed.\nPress any key to continue...")
    screen.refresh()
    screen.getch()


def delete_task(screen):
    screen.clear()
    center_text(screen, "Enter the task number to delete: ")
    screen.refresh()
    curses.echo()
    task_number = int(screen.getstr().decode("utf-8"))
    if task_number in TASKS:
        del TASKS[task_number]
        screen.clear()
        center_text(screen, "Task deleted successfully.\nPress any key to continue...")
    else:
        screen.clear()
        center_text(screen, "Task not found.\nPress any key to continue...")
    screen.refresh()
    screen.getch()
    curses.noecho()


def main(screen):
    curses.curs_set(1)  # Show cursor
    while True:
        screen.clear()
        center_text(screen, "Welcome to work timer")
        center_text(screen, "1. Add task", 1)
        center_text(screen, "2. List tasks", 3)  # Increase vertical spacing
        center_text(screen, "3. Delete task", 5)
        center_text(screen, "4. Start work", 7)
        center_text(screen, "5. Exit", 9)
        center_text(screen, "Enter a number: ", 11)
        screen.refresh()

        number = screen.getch()

        if number == ord('1'):
            add_task(screen)
        elif number == ord('2'):
            screen.clear()
            print_tasks(screen)
            center_text(screen, "\nPress any key to continue...", 4 * len(TASKS) + 2)
            screen.refresh()
            screen.getch()
        elif number == ord('3'):
            delete_task(screen)
        elif number == ord('4'):
            start_task(screen)
        elif number == ord('5'):
            screen.clear()
            center_text(screen, "Exiting the work timer.")
            screen.refresh()
            time.sleep(2)
            break
        else:
            screen.clear()
            center_text(screen, "Invalid option. Please try again.\nPress any key to continue...", 1)
            screen.refresh()
            screen.getch()


if __name__ == '__main__':
    curses.wrapper(main)
