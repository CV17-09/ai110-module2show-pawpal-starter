from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Owner:
    name: str
    available_time: int  # minutes per day
    preferences: Dict[str, str] = field(default_factory=dict)

    def update_preferences(self, **new_prefs) -> None:
        """Update owner care preferences."""
        self.preferences.update(new_prefs)

    def set_available_time(self, minutes: int) -> None:
        """Set owner available time for scheduling tasks."""
        self.available_time = minutes


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def update_info(
        self,
        name: Optional[str] = None,
        species: Optional[str] = None,
        age: Optional[int] = None,
    ) -> None:
        """Update pet details."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int
    category: str

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        category: Optional[str] = None,
    ) -> None:
        """Update task details."""
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if category is not None:
            self.category = category

    def display_task(self) -> str:
        """Return a readable string for the task."""
        return f"{self.name} ({self.category}) - {self.duration} min, priority={self.priority}"


class Scheduler:
    def __init__(self, tasks: Optional[List[Task]] = None, available_time: int = 0):
        self.tasks: List[Task] = tasks or []
        self.available_time = available_time

    def generate_plan(self) -> List[Task]:
        """Generate a daily plan based on priority and available time."""
        filtered_tasks = self.filter_tasks_by_time()
        sorted_tasks = self.sort_tasks_by_priority(filtered_tasks)

        plan: List[Task] = []
        remaining_time = self.available_time

        for task in sorted_tasks:
            if task.duration <= remaining_time:
                plan.append(task)
                remaining_time -= task.duration

        return plan

    def sort_tasks_by_priority(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks by priority, then by shorter duration."""
        tasks = tasks if tasks is not None else self.tasks
        return sorted(tasks, key=lambda task: (-task.priority, task.duration))

    def filter_tasks_by_time(self, max_time: Optional[int] = None) -> List[Task]:
        """Return tasks that can fit within the time limit individually."""
        cutoff = max_time if max_time is not None else self.available_time
        return [task for task in self.tasks if task.duration <= cutoff]

    def explain_plan(self, plan: Optional[List[Task]] = None) -> str:
        """Explain the generated plan."""
        plan = plan if plan is not None else self.generate_plan()

        if not plan:
            return "No tasks fit within the available time."

        lines = [f"The plan includes {len(plan)} task(s) within {self.available_time} available minutes."]
        lines.append("Tasks were selected based on priority and available time:")

        for task in plan:
            lines.append(f"- {task.display_task()}")

        return "\n".join(lines)