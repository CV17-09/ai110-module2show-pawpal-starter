from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a single pet care task."""

    description: str
    time_required: int  # minutes
    frequency: str
    due_date: datetime
    scheduled_time: str
    completed: bool = False
    priority: int = 1

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Marks the task as incomplete."""
        self.completed = False

    def is_recurring(self) -> bool:
        """Returns whether the task repeats on a schedule."""
        return self.frequency.lower() in ["daily", "weekly"]

    def create_next_instance(self) -> Optional["Task"]:
        """Creates the next occurrence of a recurring task."""
        frequency = self.frequency.lower()

        if frequency == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif frequency == "weekly":
            next_due_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            time_required=self.time_required,
            frequency=self.frequency,
            due_date=next_due_date,
            scheduled_time=self.scheduled_time,
            completed=False,
            priority=self.priority,
        )

    def display_task(self) -> str:
        """Returns a readable string for the task."""
        status = "Completed" if self.completed else "Pending"
        return (
            f"{self.description} | {self.time_required} min | "
            f"{self.frequency} | Due {self.due_date.strftime('%Y-%m-%d')} | "
            f"At {self.scheduled_time} | Priority {self.priority} | {status}"
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
        self.tasks = [
            task for task in self.tasks if task.description != task_description
        ]

    def get_tasks(self) -> List[Task]:
        """Returns all tasks assigned to the pet."""
        return self.tasks

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Returns tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def complete_task(self, task_description: str) -> bool:
        """Completes a task and creates the next recurring instance if needed."""
        for task in self.tasks:
            if task.description == task_description and not task.completed:
                task.mark_complete()
                new_task = task.create_next_instance()

                if new_task is not None:
                    self.tasks.append(new_task)

                return True
        return False

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

    def get_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Returns a pet by name if it exists."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Collects all tasks from all of the owner's pets."""
        all_tasks: List[Task] = []
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

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filters tasks by completion status and/or pet name."""
        if pet_name:
            pet = self.owner.get_pet_by_name(pet_name)
            tasks = pet.get_tasks() if pet else []
        else:
            tasks = self.retrieve_all_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        return tasks

    def filter_tasks_due_today(
        self,
        completed: Optional[bool] = False,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Returns tasks due today, optionally filtered by status or pet."""
        today = datetime.now().date()
        tasks = self.filter_tasks(completed=completed, pet_name=pet_name)
        return [task for task in tasks if task.due_date.date() == today]

    def get_recurring_tasks(self) -> List[Task]:
        """Returns all recurring tasks."""
        return [task for task in self.retrieve_all_tasks() if task.is_recurring()]

    def sort_by_time(self, tasks: List[Task], shortest_first: bool = True) -> List[Task]:
        """Sorts tasks by their time requirement."""
        return sorted(
            tasks,
            key=lambda task: task.time_required,
            reverse=not shortest_first,
        )

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by priority and then by shorter duration."""
        return sorted(tasks, key=lambda task: (-task.priority, task.time_required))

    def detect_time_conflict(self, tasks: List[Task]) -> bool:
        """Checks if total task time exceeds the owner's available time."""
        total_time = sum(task.time_required for task in tasks)
        return total_time > self.owner.available_time

    def detect_schedule_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return warnings for tasks scheduled at the same date and time."""
        tasks = tasks or self.retrieve_all_tasks()

        warnings: List[str] = []
        seen = {}

        for task in tasks:
            key = (task.due_date.date(), task.scheduled_time)

            if key in seen:
                other_task = seen[key]
                warnings.append(
                    f"⚠️ Conflict: '{task.description}' conflicts with "
                    f"'{other_task.description}' on "
                    f"{task.due_date.strftime('%Y-%m-%d')} at {task.scheduled_time}"
                )
            else:
                seen[key] = task

        return warnings

    def generate_plan(
        self,
        pet_name: Optional[str] = None,
        completed: bool = False,
        sort_by: str = "priority",
        due_today: bool = True,
    ) -> List[Task]:
        """Builds a daily plan using filters and sorting rules."""
        if due_today:
            tasks = self.filter_tasks_due_today(completed=completed, pet_name=pet_name)
        else:
            tasks = self.filter_tasks(completed=completed, pet_name=pet_name)

        if sort_by == "time":
            tasks = self.sort_by_time(tasks)
        else:
            tasks = self.sort_tasks_by_priority(tasks)

        selected_tasks: List[Task] = []
        remaining_time = self.owner.available_time

        for task in tasks:
            if task.time_required <= remaining_time:
                selected_tasks.append(task)
                remaining_time -= task.time_required

        return selected_tasks

    def explain_plan(self, plan: List[Task]) -> str:
        """Explains why the selected tasks were included in the plan."""
        if not plan:
            return "No tasks fit within the available time."

        total_time = sum(task.time_required for task in plan)
        lines = [
            f"The scheduler selected {len(plan)} task(s) using the owner's {self.owner.available_time} available minutes.",
            f"Total scheduled time: {total_time} minutes.",
            "Tasks were chosen based on priority or duration while fitting within the available time.",
        ]

        for task in plan:
            lines.append(f"- {task.display_task()}")

        return "\n".join(lines)