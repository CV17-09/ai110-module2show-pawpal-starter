Owner
- attributes: name, available_time, preferences
- methods: update_preferences(), set_available_time()

Pet
- attributes: name, species, age
- methods: update_info()

Task
- attributes: name, duration, priority, category
- methods: update_task(), display_task()

Scheduler
- attributes: tasks, available_time
- methods: generate_plan(), sort_tasks_by_priority(), explain_plan()

classDiagram
    class Owner {
        - name: String
        - available_time: Number
        - preferences: Map
        + update_preferences(): void
        + set_available_time(t: Number): void
    }

    class Pet {
        - name: String
        - species: String
        - age: Number
        + update_info(name: String, species: String, age: Number): void
    }

    class Task {
        - name: String
        - duration: Number
        - priority: Number
        - category: String
        + update_task(name: String, duration: Number, priority: Number, category: String): void
        + display_task(): String
    }

    class Scheduler {
        - tasks: List~Task~
        - available_time: Number
        + generate_plan(): List~Task~
        + sort_tasks_by_priority(): List~Task~
        + filter_tasks_by_time(): List~Task~
        + explain_plan(): String
    }

    Owner "1" -- "*" Pet : owns
    Owner "1" -- "*" Task : manages
    Scheduler "1" o-- "*" Task : schedules
    Scheduler "1" .. "1" Owner : uses
    Scheduler "1" .. "1" Pet : supports