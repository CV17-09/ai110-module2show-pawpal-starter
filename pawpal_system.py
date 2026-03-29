from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    time_required: int  # minutes
    frequency: str
    completed: bool = False
    priority: int = 1

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def display_task(self) -> str:
        status = "Completed" if self.completed else "Pending"
        return (
            f"{self.description} | {self.time_required} min | "
            f"{self.frequency} | Priority {self.priority} | {status}"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> None:
        self.tasks = [task for task in self.tasks if task.description != task_description]

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def update_info(self, name: str, species: str, age: int) -> None:
        self.name = name
        self.species = species
        self.age = age


@dataclass
class Owner:
    name: str
    available_time: int  # minutes per day
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_preferences(self, preferences: List[str]) -> None:
        self.preferences = preferences

    def set_available_time(self, time_minutes: int) -> None:
        self.available_time = time_minutes


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def retrieve_all_tasks(self) -> List[Task]:
        return self.owner.get_all_tasks()

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda task: (-task.priority, task.time_required))

    def generate_plan(self) -> List[Task]:
        tasks = self.retrieve_all_tasks()
        pending_tasks = [task for task in tasks if not task.completed]
        sorted_tasks = self.sort_tasks_by_priority(pending_tasks)

        selected_tasks = []
        remaining_time = self.owner.available_time

        for task in sorted_tasks:
            if task.time_required <= remaining_time:
                selected_tasks.append(task)
                remaining_time -= task.time_required

        return selected_tasks

    def explain_plan(self, plan: List[Task]) -> str:
        if not plan:
            return "No tasks fit within the available time."

        lines = [
            f"The scheduler selected {len(plan)} task(s) based on priority and available time."
        ]
        for task in plan:
            lines.append(f"- {task.display_task()}")
        return "\n".join(lines)