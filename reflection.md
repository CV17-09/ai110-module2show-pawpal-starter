# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design focused on separating the system into clear components. I created classes such as `Pet`, `Owner`, `Task`, and `Scheduler`. The `Pet` and `Owner` classes were responsible for storing basic information, while the `Task` class represented individual care activities like feeding, walking, or medication, including attributes such as duration and priority. The `Scheduler` class was responsible for generating a daily plan by selecting and organizing tasks based on constraints.

**b. Design changes**

During implementation, I realized that some responsibilities needed to be simplified. For example, I initially considered placing scheduling logic inside the `Task` class, but this made the design confusing and less modular. I moved all planning logic into the `Scheduler` class so that tasks remained simple data objects. This made the system easier to maintain and extend.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers constraints such as available time, task duration, and task priority. It may also consider user preferences, such as prioritizing certain types of activities. Priority was treated as the most important constraint because some tasks, like feeding or medication, are essential and cannot be skipped.

**b. Tradeoffs**

One tradeoff the scheduler makes is prioritizing high-priority tasks over fitting in as many tasks as possible. This means that lower-priority tasks may be excluded if there is not enough time. This tradeoff is reasonable because ensuring essential pet care tasks are completed is more important than maximizing the total number of tasks.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools to help brainstorm system design ideas, structure my classes, and refine my scheduling logic. AI was also useful for debugging and improving code readability. The most helpful prompts were specific questions about how to structure classes or how to approach scheduling logic step by step.

**b. Judgment and verification**

There were moments when I did not accept AI suggestions directly, especially when they added unnecessary complexity. I evaluated suggestions by checking if they aligned with the project requirements and testing them in my code. If a solution did not simplify the design or improve functionality, I modified or rejected it.

---

## 4. Testing and Verification

**a. What you tested**

I tested key behaviors such as whether the scheduler correctly prioritizes high-priority tasks, whether it respects time constraints, and whether tasks are properly included or excluded based on available time. These tests were important to ensure the scheduling logic behaves as expected.

**b. Confidence**

I am fairly confident that my scheduler works correctly for the main scenarios. However, there are edge cases I would test further, such as handling tasks with equal priority, very limited time availability, or conflicting constraints between tasks.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the overall system structure, especially separating responsibilities between classes. This made the project easier to understand and implement.

**b. What you would improve**

If I had another iteration, I would improve the scheduling algorithm to handle more complex constraints and make the plan more optimized. I would also enhance the explanation of why tasks were selected to make the system more transparent.

**c. Key takeaway**

One important thing I learned is the importance of designing the system clearly before implementing it. Having a solid structure made the coding process much smoother. I also learned that AI is helpful for guidance, but it is important to critically evaluate its suggestions.

## Building Blocks

The main objects in the PawPal+ system are Owner, Pet, Task, and Scheduler.

