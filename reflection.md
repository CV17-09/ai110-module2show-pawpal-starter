# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design focused on separating the system into clear components. I created classes such as `Pet`, `Owner`, `Task`, and `Scheduler`. The `Pet` and `Owner` classes were responsible for storing basic information, while the `Task` class represented individual care activities like feeding, walking, or medication, including attributes such as duration and priority. The `Scheduler` class was responsible for generating a daily plan by selecting and organizing tasks based on constraints.

**b. Design changes**

During implementation, I realized that some responsibilities needed to be simplified. For example, I initially considered placing scheduling logic inside the `Task` class, but this made the design confusing and less modular. I moved all planning logic into the `Scheduler` class so that tasks remained simple data objects.

As I expanded the system, I added new features such as recurring tasks and conflict detection. To support this, I introduced attributes like `due_date` and `scheduled_time` in the `Task` class and added logic in the `Pet` and `Scheduler` classes to handle task completion, recurrence, and scheduling conflicts. These changes made the system more realistic and flexible.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers constraints such as available time, task duration, task priority, and whether a task is completed. It also filters tasks by pet and only schedules tasks that are due for the current day. Priority is treated as the most important constraint because essential tasks like feeding or medication must be completed.

The system also includes logic for recurring tasks, where daily or weekly tasks are automatically recreated after completion with updated due dates.

**b. Tradeoffs**

One tradeoff my scheduler makes is that it only detects conflicts when two tasks have the exact same scheduled time and date. It does not detect partial overlaps, such as one task starting at 9:00 AM and another at 9:15 AM while the first task is still ongoing.

This tradeoff is reasonable because it keeps the logic simple and easy to understand while still identifying obvious scheduling conflicts. A more advanced solution could consider overlapping durations, but that would increase complexity.

---

## 3. AI Collaboration

**a. How you used AI**

I used VS Code Copilot throughout the project to support different stages of development, including system design, code generation, debugging, and refactoring. The most effective features were:

- **Inline Chat / Agent Mode** for generating class skeletons and implementing methods step by step.
- **Code suggestions** for quickly writing repetitive logic such as filtering, sorting, and task handling.
- **Targeted prompts** (e.g., asking how the Scheduler should retrieve tasks from pets) which helped clarify system interactions.

These tools helped speed up development while still allowing me to focus on the overall system design.

**b. Judgment and verification**

One example where I modified an AI suggestion was in the conflict detection logic. The AI initially suggested storing partial data (like task descriptions and metadata using dictionary access such as `__dict__`). I chose to simplify this by storing full task objects instead, which made the code cleaner, easier to read, and more maintainable.

I evaluated AI suggestions by:
- Testing them in my code
- Checking if they matched project requirements
- Deciding whether they improved readability and structure

If a suggestion added unnecessary complexity, I simplified or rejected it.

**c. Organization and workflow**

Using separate chat sessions for different phases of the project helped me stay organized and focused. For example:
- One session focused on system design and UML
- Another focused on implementation
- Another on testing and refinement

This prevented confusion and made it easier to track decisions and progress without mixing unrelated ideas.

**d. Key takeaway about AI collaboration**

One important lesson I learned is that AI is a powerful assistant, but not a decision-maker. As the developer, I needed to act as the “lead architect” by making final decisions about system structure, tradeoffs, and code clarity.

AI helped generate ideas and accelerate development, but it was my responsibility to ensure the system remained simple, logical, and aligned with the project goals. This balance between using AI and maintaining control over design was essential for building a clean and functional system.

---

## 4. Testing and Verification

**a. What you tested**

I tested key behaviors such as task completion, adding tasks to pets, filtering by status and pet, sorting tasks by time, and generating a schedule within the available time. I also tested recurring task behavior to ensure that completing a task creates a new instance with an updated due date, and conflict detection to verify that warnings are generated when tasks share the same scheduled time.

These tests were important to ensure both core functionality and advanced features worked correctly.

**b. Confidence**

I am fairly confident that my scheduler works correctly for the main scenarios. However, there are edge cases I would test further, such as overlapping task durations, tasks with equal priority, or more complex recurrence patterns.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the system structure and how responsibilities are clearly separated between classes. This made it easier to implement new features like filtering, sorting, recurrence, and conflict detection without breaking existing functionality.

**b. What you would improve**

If I had another iteration, I would improve the scheduling algorithm to handle more complex time-based conflicts, including overlapping durations. I would also improve how the system explains its decisions to make it more user-friendly.

**c. Key takeaway**

One important thing I learned is the importance of designing a clear system before implementing it. This made development smoother and easier to extend. I also learned that AI is helpful for guidance, but it is important to critically evaluate its suggestions.

---

## Building Blocks

The main objects in the PawPal+ system are `Owner`, `Pet`, `Task`, and `Scheduler`.

