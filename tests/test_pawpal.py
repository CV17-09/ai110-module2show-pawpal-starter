from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    task = Task("Feed Dog", 10, "Daily", datetime.now(), "08:00", priority=5)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(name="Buddy", species="Dog", age=3)

    task = Task("Walk Dog", 30, "Daily", datetime.now(), "09:00", priority=4)

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_filter_tasks_by_status():
    owner = Owner(name="Claudia", available_time=60)
    pet = Pet(name="Buddy", species="Dog", age=3)

    task1 = Task("Feed Dog", 10, "Daily", datetime.now(), "08:00", completed=False, priority=5)
    task2 = Task("Give Treat", 5, "Daily", datetime.now(), "12:00", completed=True, priority=2)

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    pending_tasks = scheduler.filter_tasks(completed=False)

    assert len(pending_tasks) == 1
    assert pending_tasks[0].description == "Feed Dog"


def test_filter_tasks_by_pet():
    owner = Owner(name="Claudia", available_time=60)
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    dog_task = Task("Walk Dog", 30, "Daily", datetime.now(), "09:00", priority=5)
    cat_task = Task("Play with Cat", 20, "Daily", datetime.now(), "10:00", priority=3)

    dog.add_task(dog_task)
    cat.add_task(cat_task)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")

    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].description == "Walk Dog"


def test_sort_tasks_by_time():
    owner = Owner(name="Claudia", available_time=60)
    scheduler = Scheduler(owner)

    task1 = Task("Walk Dog", 30, "Daily", datetime.now(), "09:00", priority=5)
    task2 = Task("Feed Dog", 10, "Daily", datetime.now(), "08:00", priority=5)
    task3 = Task("Play with Cat", 20, "Daily", datetime.now(), "10:00", priority=3)

    tasks = [task1, task2, task3]
    sorted_tasks = scheduler.sort_by_time(tasks)

    assert sorted_tasks[0].description == "Feed Dog"
    assert sorted_tasks[1].description == "Play with Cat"
    assert sorted_tasks[2].description == "Walk Dog"


def test_get_recurring_tasks():
    owner = Owner(name="Claudia", available_time=60)
    pet = Pet(name="Buddy", species="Dog", age=3)

    task1 = Task("Feed Dog", 10, "Daily", datetime.now(), "08:00", priority=5)
    task2 = Task("Vet Visit", 45, "Once", datetime.now(), "14:00", priority=4)

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    recurring_tasks = scheduler.get_recurring_tasks()

    assert len(recurring_tasks) == 1
    assert recurring_tasks[0].description == "Feed Dog"


def test_detect_time_conflict():
    owner = Owner(name="Claudia", available_time=20)
    pet = Pet(name="Buddy", species="Dog", age=3)

    task1 = Task("Walk Dog", 15, "Daily", datetime.now(), "09:00", priority=5)
    task2 = Task("Feed Dog", 10, "Daily", datetime.now(), "10:00", priority=4)

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tasks = scheduler.filter_tasks(completed=False)

    assert scheduler.detect_time_conflict(tasks) is True


def test_generate_plan_respects_available_time():
    owner = Owner(name="Claudia", available_time=30)
    pet = Pet(name="Buddy", species="Dog", age=3)

    task1 = Task("Walk Dog", 25, "Daily", datetime.now(), "09:00", priority=5)
    task2 = Task("Feed Dog", 10, "Daily", datetime.now(), "08:00", priority=4)
    task3 = Task("Brush Fur", 15, "Weekly", datetime.now(), "11:00", priority=3)

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    total_time = sum(task.time_required for task in plan)
    assert total_time <= owner.available_time


def test_daily_task_creates_next_instance():
    pet = Pet(name="Buddy", species="Dog", age=3)
    today = datetime.now()

    task = Task("Morning Walk", 30, "Daily", today, "09:00", priority=5)
    pet.add_task(task)

    pet.complete_task("Morning Walk")

    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].due_date.date() == (today + timedelta(days=1)).date()


def test_detect_schedule_conflicts_returns_warning_for_same_time():
    owner = Owner(name="Claudia", available_time=60)
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    today = datetime.now()

    dog.add_task(Task("Morning Walk", 30, "Daily", today, "09:00", priority=5))
    cat.add_task(Task("Play with Cat", 20, "Daily", today, "09:00", priority=3))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_schedule_conflicts()

    assert len(warnings) == 1
    assert "conflicts with" in warnings[0]
    assert "09:00" in warnings[0]


def test_detect_schedule_conflicts_returns_empty_when_no_overlap():
    owner = Owner(name="Claudia", available_time=60)
    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    today = datetime.now()

    dog.add_task(Task("Morning Walk", 30, "Daily", today, "09:00", priority=5))
    cat.add_task(Task("Play with Cat", 20, "Daily", today, "10:00", priority=3))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_schedule_conflicts()

    assert warnings == []