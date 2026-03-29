from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""

    description: str
    time_required: int  # minutes
    frequency: str
    completed: bool = False
    priority: int = 1

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Marks the task as incomplete."""
        self.completed = False

    def display_task(self) -> str:
        """Returns a readable string for the task."""
        status = "Completed" if self.completed else "Pending"
        return (
            f"{self.description} | {self.time_required} min | "
            f"{self.frequency} | Priority {self.priority} | {status}"
        )


@dataclass
class Pet:
    """Stores pet details and its care tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> None:
        """Removes a task by its description."""
        self.tasks = [task for task in self.tasks if task.description != task_description]

    def get_tasks(self) -> List[Task]:
        """Returns all tasks assigned to the pet."""
        return self.tasks

    def update_info(self, name: str, species: str, age: int) -> None:
        """Updates the pet's basic information."""
        self.name = name
        self.species = species
        self.age = age


@dataclass
class Owner:
    """Represents a pet owner and the pets they manage."""

    name: str
    available_time: int  # minutes per day
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Removes a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Collects all tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_preferences(self, preferences: List[str]) -> None:
        """Updates the owner's care preferences."""
        self.preferences = preferences

    def set_available_time(self, time_minutes: int) -> None:
        """Sets the owner's available time for the day."""
        self.available_time = time_minutes


class Scheduler:
    """Generates a daily task plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Initializes the scheduler with an owner."""
        self.owner = owner

    def retrieve_all_tasks(self) -> List[Task]:
        """Retrieves all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by priority and then by shorter duration."""
        return sorted(tasks, key=lambda task: (-task.priority, task.time_required))

    def generate_plan(self) -> List[Task]:
        """Builds a daily plan based on priority and available time."""
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
        """Explains why the selected tasks were included in the plan."""
        if not plan:
            return "No tasks fit within the available time."

        lines = [
            f"The scheduler selected {len(plan)} task(s) based on priority and available time."
        ]
        for task in plan:
            lines.append(f"- {task.display_task()}")
        return "\n".join(lines)