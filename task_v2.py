"""Task Management System - V1 + V2

Use case:
Manage tasks in memory through a console menu

Main entity:
Task

Task fields:
task_id: int
title: str
description: str
status: str

Allowed statuses:
- pending
- in_progress
- completed

Layers:
- Domain exceptions: TaskAlreadyExistsError, TaskNotFoundError, InvalidTaskStatusError
- Domain model: Task
- Service Layer: TaskManager
- Interface: console menu and input/output functions
- Orchestration: main():

Main actions:
- Add task
- List tasks
- Search task by ID
- Update task status
- Delete task

Validation strategy:
1. The interface validates basic user input from the console.
2. The Task entity validates its own fields to protect object consistency.
3. The TaskManager service validates business rules such as duplicated IDs, and missing tasks.

Manual test cases:
- Add task with duplicated ID. -> TaskAlreadyExistsError
- Add task with empty title.
- Add task with empty status.
- Add task with invalid status. -> InvalidTaskStatusError
- Search non-existing task. -> TaskNotFoundError
- Update non-existing task.
- Update task with invalid status.
- Delete non existing task.
"""

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

# DOMAIN MODEL
class Task:
    """Domain entity represent a task"""
    
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

    def __str__(self) -> str:
        return(
            f"[{self.task_id}] {self.title} | "
            f"Description: {self.description} | "
            f"Status: {self.status}"
        )

# SERVICE LAYER
"""
- Add task
- List tasks
- Search task by ID
- Update task status
- Delete task
"""
class TaskManager:
    """Coordinates operations for task."""
    
    def __init__(self):
        self._tasks_by_id: dict[int, Task] = {}
        
    def add_task(self, task: Task) -> None:
        """Adds a task.
        
        Raises:
            TaskAlreadyExistsError: if the task already exists
        """
        if task.task_id not in self._tasks_by_id:
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
    
    def delete_task(self, task_id: int) -> None:
        """Removes a task from the system."""
        if task_id not in self._tasks_by_id:
            raise TaskNotFoundError(
                f"Task with ID {task_id} was not found"
            )

        del self._tasks_by_id[task_id]
        
# INTERFACE
def show_menu() -> None:
    print("\n=== TASKS MANAGER SYSTEM (V2) ===")
    print("1. Add task.")
    print("2. List tasks.")
    print("3. Finds task by ID.")
    print("4. Update task status.")
    print("5. Delete task.")
    print("0. Exit.")
    
def ask_option() -> str:
    while True:
        option = input("Choose an option: ".strip())
        
        if option in ("0", "1", "2", "3", "4", "5"):
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
    task_id = ask_positive_int("Task ID: ")
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
def main():
    manager = TaskManager()
    
    while True:
        show_menu()
        option = ask_option()
        
        if option == "0":
            print("Exiting task manager system.")
            break
        
        elif option == "1":
            try:
                task = ask_task_data() # creates a task
                manager.add_task(task) # store a task
            
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
                print("Task status updated sucessfully")
            
            except TaskNotFoundError as error:
                print(error)
            
            except InvalidTaskStatusError as error:
                print(error)
                
        elif option == "5":
            task_id = ask_positive_int("Task ID: ")
            
            try:
                manager.delete_task(task_id)
                print("Task deleted successfully.")
            except TaskNotFoundError as error:
                print(error)

if __name__ == "__main__":
    main()
