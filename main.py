from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create owner
    owner = Owner(name="Claudia", available_time=60)  # 60 minutes

    # Create pets
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks
    task1 = Task(description="Morning Walk", time_required=30, frequency="Daily", priority=5)
    task2 = Task(description="Feed Dog", time_required=10, frequency="Daily", priority=5)
    task3 = Task(description="Play with Cat", time_required=20, frequency="Daily", priority=3)

    # Assign tasks to pets
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate plan
    plan = scheduler.generate_plan()

    # Print schedule
    print("\n🐾 Today's Schedule:\n")

    if not plan:
        print("No tasks fit within the available time.")
    else:
        for i, task in enumerate(plan, start=1):
            print(f"{i}. {task.display_task()}")

    # Print explanation
    print("\n🧠 Explanation:\n")
    print(scheduler.explain_plan(plan))


if __name__ == "__main__":
    main()