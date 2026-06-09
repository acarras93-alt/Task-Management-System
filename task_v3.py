"""
Task Management System - Version 3

Main goal:
Add JSON persistence to the task system while keeping a clean backend-style architecture.

Layers: 
- Exceptions Domain: TaskAlreadyExistsError, TaskNotFoundError, InvalidTaskStatusError
- Domain Model: Task
- Service Layer: TaskManager
- Persistence: JSONTaskStorage
- Interface: console menu and input/output functions
- Orchestation: main()

V3 improvements:
- Tasks can be converted to dictionaries using Task.to_dict().
- Tasks can be restored from diccionaries using Task.from_dict().
- Task data is loaded from a JSON file when the program starts.
- Task data is saved to a JSON file after add, update, and delete operations.
- TaskManager keeps using dict[int, Task] internally.
- JSON persistence uses list[dict] only for serialization.

Validation strategy:
1. The interface validates user input before creating or updating taks.
2. The Task entity validates its own fields to protect objetct consistency.
3. The service layer validates business rules such as duplicated IDs or missing taks.
4. The persistence layer converts between Task objects and JSON-compatible dictionaries.

Manual test cases:
- Start the program with no JSON file.
- Add a valid task.
- Add a task with a duplicated ID.
- Add a task with a wrong status.
- Search for an existing task.
- Search for a non_existing task.
- Delete an existing task.
- Delete an non-existing task.
- Exit the program and verify that task_data.json is created.
- Run the program again and verify that saved tasks are loaded correctly.
"""

import json
from pathlib import Path

# EXCEPTIONS DOMAIN
class TaskAlreadyExistsError(Exception):
    """Raised when trying to add a task with an existing ID."""
    pass

class TaskNotFoundError(Exception):
    """Raised when a task cannot be found."""
    pass

class InvalidTaskStatusError(Exception):
    """Raised when a task has a invalid status."""
    pass

class TasksStorageError(Exception):
    """Raised when task persistence operations fail."""
    pass

# DOMAIN MODEL
class Task:
    """Domain entity that represent a task."""
    
    VALID_STATUSES = ("pending", "in_progress", "completed")
    
    def __init__(
        self,
        task_id: int, # Validated at creation and protected afterwards
        title: str, # Can be modified, but validated
        description: str, # Can be modified, but validated
        status: str # Can be modified, bat validated
    ):
        self._task_id = self._validate_task_id(task_id)
        self._title = self._validate_title(title)
        self._description = self._validate_description(description)
        self._status = self._validate_status(status)
        
    @staticmethod
    def _validate_task_id(task_id: int) -> int:
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        
        if task_id < 0:
            raise ValueError("Task ID must be 0 or greater.")
        
        return task_id
    
    @staticmethod
    def _validate_title(title: str) -> str:
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        
        title = title.strip()
        
        if not title:
            raise ValueError("Title cannot be empty.")
        
        return title
    
    @staticmethod
    def _validate_description(description: str) -> str:
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        
        description = description.strip()
        
        if not description:
            raise ValueError("Description cannot be empty.")
        
        return description
    
    @staticmethod
    def _validate_status(status: str) -> str:
        if not isinstance(status, str):
            raise TypeError("Status must be a string.")
        
        status = status.strip()
        
        if not status:
            raise ValueError("Status cannot be empty.")
        
        if status not in Task.VALID_STATUSES:
            raise InvalidTaskStatusError(
                f"Invalid status. Allowed statuses: {Task.VALID_STATUSES}"
            )
        return status
        
    @property
    def task_id(self) -> int:
        return self._task_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = self._validate_title(value)
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        self._description = self._validate_description(value)
        
    @property
    def status(self) -> str:
        return self._status
    
    @status.setter
    def status(self, value: str) -> None:
        self._status = self._validate_status(value)
        
    def update_status(self, new_status: str) -> None:
        self.status = new_status
    
    def update_description(self, new_description: str) -> None:
        self.description = new_description
    
    def rename(self, new_title: str) -> None:
        self.title = new_title
    
    def update_details(self, new_title: str, new_description: str) -> None:
        self.title = new_title
        self.description = new_description

    def to_dict(self) -> dict[str, int | str]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task_id = data["task_id"]
        title = data["title"]
        description = data["description"]
        status = data["status"]

        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if not isinstance(title, str):
            raise TypeError("Title must be a string.")

        if not isinstance(description, str):
            raise TypeError("Description must be a string.")

        if not isinstance(status, str):
            raise TypeError("Status must be a string.")

        return cls(
            task_id=task_id,
            title=title,
            description=description,
            status=status
        )

# SERVICE LAYER
class TaskManager:
    """Coordinates operations for task."""
    
    def __init__(self):
        self._tasks_by_id: dict[int, Task] = {}
        
    def add_task(self, task: Task) -> None:
        """Adds a task.
        
        Raises:
            TaskAlreadyExistsError: if the task already exists
        """
        if task.task_id in self._tasks_by_id:
            raise TaskAlreadyExistsError(
                f"Task with ID {task.task_id} already exists."
            )

        self._tasks_by_id[task.task_id] = task
        
    def list_tasks(self) -> list[Task]:
        """Returns all tasks currently stored in the system."""
        return list(self._tasks_by_id.values())
    
    def find_task_by_id(self, task_id: int) -> Task:
        """Finds a task by its ID.
        
        Raises:
            TaskNotFoundError: if the task does not exist
        """
        task = self._tasks_by_id.get(task_id)
        
        if task is None:
            raise TaskNotFoundError(
                f"Task with ID {task_id} was not found"
            )
        
        return task
    
    def update_task_status(self, task_id: int, new_status: str) -> None:
        """Updates the status of an existing task."""
        task = self.find_task_by_id(task_id)
        task.update_status(new_status)
    
    def rename_task(self, task_id: int, new_title: str) -> None:
        """Renames an existing task."""
        task = self.find_task_by_id(task_id)
        task.rename(new_title)
        
    def update_task_description(self, task_id: int, new_description: str) -> None:
        """Updates the description of an existing task."""
        task = self.find_task_by_id(task_id)
        task.update_description(new_description)
        
    def update_task_details(
        self,
        task_id: int,
        new_title: str,
        new_description: str
    ) -> None:
        """Updates the title and description of an existing task."""
        task = self.find_task_by_id(task_id)
        task.update_details(new_title, new_description)
    
    def delete_task(self, task_id: int) -> None:
        """Removes a task from the system."""
        if task_id not in self._tasks_by_id:
            raise TaskNotFoundError(
                f"Task with ID {task_id} was not found"
            )
        del self._tasks_by_id[task_id]
    
    def load_tasks(self, tasks: list[Task]) -> None:
        """Loads multiple tasks into the task manager."""
        for task in tasks:
            self.add_task(task)
            
# PERSISTENCE LAYER
class JSONTasksStorage:
    """Handles task management persistence using JSON file"""
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
    
    def save_tasks(self, tasks: list[Task]) -> None:
        """Saves a list of Taks objects into a JSON file"""
        tasks_data = []
        
        for task in tasks:
            tasks_data.append(task.to_dict())
        
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks_data, file, indent=4)
    
    def load_tasks(self) -> list[Task]:
        """Loads taks from a JSON file
        
        If the file does not exist, return an empty list.
        
        Raises:
            TaskStorageError: if the file cannot be read or contains invalid data.
        """
        if not self.file_path.exists():
            return []
        
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                
                tasks = []
                
                for task_data in tasks_data:
                    task = Task.from_dict(task_data)
                    tasks.append(task)
            
            return tasks
        
        except json.JSONDecodeError as error:
            raise TasksStorageError(f"Invalid JSON format in {self.file_path.name}: {error}") from error
        
        except (KeyError, TypeError, ValueError,  InvalidTaskStatusError) as error:
            raise TasksStorageError(f"Invalid task data structure: {error}") from error
        
# INTERFACE
def show_menu() -> None:
    print("\n=== TASKS MANAGER SYSTEM (V3) ===")
    print("1. Add task.")
    print("2. List tasks.")
    print("3. Finds task by ID.")
    print("4. Update task status.")
    print("5. Rename task.")
    print("6. Update task description.")
    print("7. Update task details")
    print("8. Delete task.")
    print("0. Exit.")
    
def ask_option() -> str:
    while True:
        option = input("Choose an option: ".strip())
        
        if option in ("0", "1", "2", "3", "4", "5", "6", "7", "8"):
            return option
        
        print("Invalid option.")

def ask_non_empty_text(message: str) -> str:
    while True:
        text = str(input(message).strip())
        
        if text:
            return text
        
        print("It cannot be empty.")

def ask_positive_int(message: str) -> int:
    while True:
        try:
            value = int(input(message).strip())

            if value >= 0:
                return value

            print("The value must be zero or greater.")

        except ValueError:
            print("Invalid number.")

def ask_task_data() -> Task:
    task_id = ask_positive_int("Task ID:")
    title = ask_non_empty_text("Title: ")
    description = ask_non_empty_text("Description: ")
    status = ask_non_empty_text("Status: ")
    
    return Task(
        task_id=task_id,
        title=title,
        description=description,
        status=status
    )

def print_task(task: Task) -> None:
    print(
        f"[{task.task_id}] {task.title} | "
        f"Description: {task.description} | "
        f"Status: {task.status}"
    )
        
def print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("There are no tasks.")
        return

    for task in tasks:
        print(
            f"[{task.task_id}] {task.title} | "
            f"Description: {task.description} | "
            f"Status: {task.status}"
        )

# ORCHESTRATION
def main() -> None:
    manager = TaskManager()
    storage = JSONTasksStorage("task_data.json")
    
    try:
        loaded_tasks = storage.load_tasks()
        manager.load_tasks(loaded_tasks)
        print("Tasks data loaded successfully.")
    
    except TasksStorageError as error:
        print(f"Could not load tasks data: {error}")
    
    while True:
        show_menu()
        option = ask_option()
        
        if option == "0":
            storage.save_tasks(manager.list_tasks())
            print("Tasks data saved successfully.")
            print("Exiting task manager system.")
            break
        
        elif option == "1":
            try:
                task = ask_task_data() # creates a task
                manager.add_task(task) # store a task
                storage.save_tasks(manager.list_tasks())
            
            except TaskAlreadyExistsError as error:
                print(error)
            
            except InvalidTaskStatusError as error:
                print(error)
            
            except(TypeError, ValueError) as error:
                print(f"Invalid task data: {error}")
        
        elif option == "2":
            tasks = manager.list_tasks()
            print_tasks(tasks)
        
        elif option == "3":
            task_id = ask_positive_int("Task ID: ")
            
            try:
                task = manager.find_task_by_id(task_id)
                print_task(task)
            
            except TaskNotFoundError as error:
                print(error)
        
        elif option == "4":
            task_id = ask_positive_int("Task ID: ")
            new_status = ask_non_empty_text("New status: ")
            
            try:
                manager.update_task_status(task_id, new_status)
                storage.save_tasks(manager.list_tasks())
                print("Task status updated sucessfully")
            
            except TaskNotFoundError as error:
                print(error)
            
            except InvalidTaskStatusError as error:
                print(error)
        
        elif option == "5":
            task_id = ask_positive_int("Task ID: ")
            new_title = ask_non_empty_text("New title: ")
            
            try:
                manager.rename_task(task_id, new_title)
                storage.save_tasks(manager.list_tasks())
                print("New title updated sucessfully")
            
            except TaskNotFoundError as error:
                print(error)
            
            except(TypeError, ValueError) as error:
                print(f"Invalid task data: {error}")
        
        elif option == "6":
            task_id = ask_positive_int("Task ID: ")
            new_description = ask_non_empty_text("New description: ")
            
            try:
                manager.update_task_description(task_id, new_description)
                storage.save_tasks(manager.list_tasks())
                print("Task description updated sucessfully")
            
            except TaskNotFoundError as error:
                print(error)
            
            except(TypeError, ValueError) as error:
                print(f"Invalid task data: {error}")
        
        elif option == "7":
            task_id = ask_positive_int("Task ID: ")
            new_title = ask_non_empty_text("New title: ")
            new_description = ask_non_empty_text("New description: ")
            
            try:
                manager.update_task_details(task_id, new_title, new_description)
                storage.save_tasks(manager.list_tasks())
                print("Task content updated sucessfully")
            
            except TaskNotFoundError as error:
                print(error)
                
            except(TypeError, ValueError) as error:
                print(f"Invalid task data: {error}")
                
        elif option == "8":
            task_id = ask_positive_int("Task ID: ")
            
            try:
                manager.delete_task(task_id)
                storage.save_tasks(manager.list_tasks())
                print("Task deleted successfully.")
            except TaskNotFoundError as error:
                print(error)

if __name__ == "__main__":
    main()