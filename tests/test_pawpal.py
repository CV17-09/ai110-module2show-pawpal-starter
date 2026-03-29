from pawpal_system import Task, Pet


def test_task_completion():
    task = Task(
        description="Feed Dog",
        time_required=10,
        frequency="Daily",
        priority=5
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(name="Buddy", species="Dog", age=3)

    task = Task(
        description="Walk Dog",
        time_required=30,
        frequency="Daily",
        priority=4
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1