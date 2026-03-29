from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(title: str, tasks: list[Task]) -> None:
    print(f"\n{title}\n")
    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.display_task()}")


def main():
    owner = Owner(name="Claudia", available_time=60)

    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    today = datetime.now()

    dog.add_task(Task("Morning Walk", 30, "Daily", today, "09:00", priority=5))
    dog.add_task(Task("Feed Dog", 10, "Daily", today, "08:00", priority=5))
    dog.add_task(Task("Brush Fur", 15, "Weekly", today, "11:00", priority=2))

    cat.add_task(Task("Play with Cat", 20, "Daily", today, "09:00", priority=3))
    cat.add_task(Task("Clean Litter Box", 15, "Daily", today, "10:00", priority=4))
    cat.add_task(Task("Give Treat", 5, "Once", today, "12:00", completed=True, priority=1))

    scheduler = Scheduler(owner)

    print_tasks("🐾 All Tasks", scheduler.retrieve_all_tasks())
    print_tasks("📅 Today's Schedule", scheduler.generate_plan())

    print("\n🧠 Explanation\n")
    print(scheduler.explain_plan(scheduler.generate_plan()))

    print("\n⚠ Conflict Warnings\n")
    warnings = scheduler.detect_schedule_conflicts()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No scheduling conflicts detected.")


if __name__ == "__main__":
    main()