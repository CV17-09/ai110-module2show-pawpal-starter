import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")


def task_to_row(task: Task) -> dict:
    """Convert a Task object into a table-friendly dictionary."""
    return {
        "Task": task.description,
        "Time Required (min)": task.time_required,
        "Frequency": task.frequency,
        "Due Date": task.due_date.strftime("%Y-%m-%d"),
        "Scheduled Time": task.scheduled_time,
        "Priority": task.priority,
        "Completed": "Yes" if task.completed else "No",
    }


def load_demo_data() -> Owner:
    """Create demo owner, pets, and tasks for the UI."""
    owner = Owner(name="Claudia", available_time=60)

    dog = Pet(name="Buddy", species="Dog", age=3)
    cat = Pet(name="Milo", species="Cat", age=2)

    today = datetime.now()

    dog.add_task(Task("Morning Walk", 30, "Daily", today, "09:00", priority=5))
    dog.add_task(Task("Feed Dog", 10, "Daily", today, "08:00", priority=5))
    dog.add_task(Task("Brush Fur", 15, "Weekly", today, "11:00", priority=2))

    cat.add_task(Task("Play with Cat", 20, "Daily", today, "09:00", priority=3))
    cat.add_task(Task("Clean Litter Box", 15, "Daily", today, "10:00", priority=4))
    cat.add_task(Task("Give Treat", 5, "Once", today, "12:00", completed=True, priority=1))

    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner


st.title("🐾 PawPal+")
st.write("A smarter pet care scheduler for organizing daily pet tasks.")

# Load data
owner = load_demo_data()
scheduler = Scheduler(owner)

# Sidebar controls
st.sidebar.header("Schedule Options")

sort_option = st.sidebar.selectbox(
    "Sort tasks by",
    ["priority", "time"]
)

pet_filter = st.sidebar.selectbox(
    "Filter by pet",
    ["All"] + [pet.name for pet in owner.pets]
)

status_filter = st.sidebar.selectbox(
    "Filter by status",
    ["All", "Pending", "Completed"]
)

due_today_only = st.sidebar.checkbox("Show only tasks due today", value=True)

# Convert sidebar selections
pet_name = None if pet_filter == "All" else pet_filter

completed_value = None
if status_filter == "Pending":
    completed_value = False
elif status_filter == "Completed":
    completed_value = True

# Build filtered task list
if due_today_only:
    filtered_tasks = scheduler.filter_tasks_due_today(
        completed=completed_value if completed_value is not None else False,
        pet_name=pet_name,
    ) if status_filter != "All" else scheduler.filter_tasks_due_today(
        completed=None,
        pet_name=pet_name,
    )
else:
    filtered_tasks = scheduler.filter_tasks(
        completed=completed_value,
        pet_name=pet_name,
    )

# Sort filtered tasks
if sort_option == "time":
    filtered_tasks = scheduler.sort_by_time(filtered_tasks)
else:
    filtered_tasks = scheduler.sort_tasks_by_priority(filtered_tasks)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Tasks")

    if filtered_tasks:
        st.table([task_to_row(task) for task in filtered_tasks])
    else:
        st.info("No tasks match the selected filters.")

    st.subheader("Today's Schedule")

    plan = scheduler.generate_plan(
        pet_name=pet_name,
        completed=False,
        sort_by=sort_option,
        due_today=due_today_only,
    )

    if plan:
        for task in plan:
            st.success(task.display_task())
    else:
        st.warning("No tasks fit within the available time.")

    st.subheader("Plan Explanation")
    st.write(scheduler.explain_plan(plan))

with col2:
    st.subheader("Owner Summary")
    st.write(f"**Owner:** {owner.name}")
    st.write(f"**Available Time:** {owner.available_time} minutes")

    st.subheader("Pets")
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species}, age {pet.age})")

    st.subheader("Recurring Tasks")
    recurring_tasks = scheduler.get_recurring_tasks()
    if recurring_tasks:
        st.table([task_to_row(task) for task in recurring_tasks])
    else:
        st.info("No recurring tasks found.")

    st.subheader("Conflict Warnings")
    warnings = scheduler.detect_schedule_conflicts()

    if warnings:
        st.warning("Some pet care tasks overlap. Review these conflicts:")
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")