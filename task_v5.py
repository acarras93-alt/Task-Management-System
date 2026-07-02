"""Task System V5
Arquitectura por capas:
- Domain:
    Task
- Domain exceptions:
    TaskAlreadyExistsError
    TaskNotFoundError
    InvalidTaskStatusError
- Infrastructure exception:
    TaskStorageError
- Repository contract:
    TaskRepository
- Repository implementations:
    InMemoryTaskRepository
    JSONTaskRepository
- Service:
    TaskService
- Interface / Orchestration:
    funciones de consola + main
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path

# EXCEPTIONS DOMAIN
class TaskAlreadyExistsError(Exception):
    """Raised when trying to add a task with an existing ID."""
    pass

class TaskNotFoundError(Exception):
    """Raised when a task cannot be found."""
    pass

class InvalidTaskStatusError(Exception):
    """Raised when a task has an invalid status."""
    pass

class TaskStorageError(Exception):
    """Raised when task persistence operations fail."""
    pass

# DOMAIN MODEL
class Task:
    """Domain entity that represents a task.
    
    Esta clase proteje sus propias reglas:
        - task_id debe ser int >= 0
        - title debe ser str no vacio
        - description debe ser str no vacio
        - status debe ser str no vacio
    """
    
    VALID_STATUSES = ("pending", "in_progress", "completed")
    
    def __init__(
        self,
        task_id: int, 
        title: str,
        description: str, 
        status: str 
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
        """Convierte la entidad a un formato serializable.
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Reconstruye una entidad Task con datos cargados
        
        Importante: aunque los datos vengan de JSON, pasan por el constructor,
        por tanto las validaciones de dominio se vuelven a aplicar.
        """
        return cls (
            task_id = data["task_id"],
            title = data["title"],
            description = data["description"],
            status = data["status"],
        )

# CONTRACT REPOSITORY
class TaskRepository(ABC):
    """Contrato del repositorio de tareas.
    
    Esta es la pieza clave de esta versión 5.
    
    El servicio sí depende de esta abstracción.
    El servicio desconoce si los datos vienen de:
        - JSON
        - Memoria
        - SQlite
        - Prostgre SQL
        - Api Externa
        
    Regla mental: TaskRepository es la puerta de acceso a la colección de tareas.
    """
    @abstractmethod
    def add(self, task: Task) -> None:
        """Add a new task to the colletion."""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        """Returns a task by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def list_all(self)-> list[Task]:
        """Returns all tasks from the collection."""
        raise NotImplementedError
    
    @abstractmethod
    def list_by_status(self, status: str) -> list[Task]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, task: Task)-> None:
        """Updates an existing task."""
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, task_id: int)-> None:
        """"""
        raise NotImplementedError
    
# IN-MEMORY REPOSITORY
class InMemoryTaskRepository(TaskRepository):
    """Repositorio en memoria
    
    Uso princial:
    - Test en memoria
    - Pruebas rápidas
    - Desarrollo sin tocar archivos
    
    Este repositorio presenta el mismo contrato que JSONTaksRepository. 
    Por eso TaskService puede trabajar con ambos.
    """
    
    def __init__(self) -> None:
        self._tasks_by_id: dict[int, Task] = {}
        
    def add(self, task: Task) -> None:
        """Adds a task.
        
        Raises:
            TaskAlreadyExistsError: if the task already exists
        """
        if task.task_id in self._tasks_by_id:
            raise TaskAlreadyExistsError(
                f"Task with ID {task.task_id} already exists."
            )

        self._tasks_by_id[task.task_id] = task
    
    def get_by_id(self, task_id: int) -> Task:
        """Finds a task by its ID.
        
        Raises:
            TaskNotFoundError: if the task does not exist
        """
        if task_id not in self._tasks_by_id:
            raise TaskNotFoundError(
                f"Task with ID {task_id} was not found."
            )
        
        return self._tasks_by_id[task_id]
        
    def list_all(self) -> list[Task]:
        """Returns all tasks currently stored in the system."""
        tasks = []
        
        for task in self._tasks_by_id.values():
            tasks.append(task)
            
        return tasks
    
    def list_by_status(self, status: str) -> list[Task]:
        # Validate the received status
        validated_status = Task._validate_status(status)
        
        tasks = []
        
        for task in self._tasks_by_id.values():
            if task.status == validated_status:
                tasks.append(task)
        
        return tasks
    
    def update(self, task: Task) -> None:
        if task.task_id not in self._tasks_by_id:
            raise TaskNotFoundError(
                f"Task with ID {task.task_id} was not found."
            )
        
        self._tasks_by_id[task.task_id] = task
    
    def delete(self, task_id: int) -> None:
        if task_id not in self._tasks_by_id:
            raise TaskNotFoundError(
                f"Task with ID {task_id} was not found."
            )
        
        del self._tasks_by_id[task_id]
            
# JSON REPOSITORY
class JSONTaskRepository(TaskRepository):
    """Implementación de JSON del respositorio.
    
    Esta clase si conoce JSON.
    Esta clase si sabe cargar y guardar.
    """
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
            
    def add(self, task: Task) -> None:
        tasks = self.list_all()
        
        for existing_task in tasks:
            if existing_task.task_id == task.task_id:
                raise TaskAlreadyExistsError(
                    f"Task with ID {task.task_id} already exists."
                )
        tasks.append(task)
        self._save_all(tasks)
    
    def get_by_id(self, task_id:int) -> Task:
        tasks = self.list_all()
        
        for task in tasks:
            if task.task_id == task_id:
                return task
        
        raise TaskNotFoundError(
            f"Task with ID {task_id} was not found."
        )
        
    def list_all(self) -> list[Task]:
        """Loads tasks from a JSON file.

        If the file does not exist, return an empty list.

        Raises:
        TasksStorageError: if the file cannot be read or contains invalid data.
        """
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                
            if not isinstance(tasks_data, list):
                raise TaskStorageError(
                    "Invalid JSON structure. Expected a list of tasks."
                )
            tasks = []

            for task_data in tasks_data:
                task = Task.from_dict(task_data)
                tasks.append(task)

            return tasks

        except json.JSONDecodeError as error:
            raise TaskStorageError(
                f"Invalid JSON format in {self.file_path.name}: {error}"
            ) from error

        except OSError as error:
            raise TaskStorageError("Tasks could not be loaded.") from error

        except KeyError as error:
            raise TaskStorageError(
                f"Invalid task data. Missing field: {error}."
            ) from error
        
        except TypeError as error:
            raise TaskStorageError(
                f"Invalid product data type: {error}."
            ) from error
        
        except ValueError as error:
            raise TaskStorageError(
                f"Invalid product value: {error}."
            ) from error
    
    def list_by_status(self, status: str) -> list[Task]:
        validated_status = Task._validate_status(status)
        tasks = self.list_all()
        filtered_tasks = []

        for task in tasks:
            if task.status == validated_status:
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def update(self, task: Task) -> None:
        tasks = self.list_all()
        updated_tasks = []
        task_was_found = False
        
        for existing_task in tasks:
            if existing_task.task_id == task.task_id:
                updated_tasks.append(task)
                task_was_found = True
            else:
                updated_tasks.append(existing_task)
            
        if not task_was_found:
            raise TaskNotFoundError(
                    f"Task with ID {task.task_id} was not found."
                )
        self._save_all(updated_tasks)
            
    def delete(self, task_id:int) -> None:
        tasks = self.list_all()
        remaining_tasks = []
        task_was_found = False
        
        for task in tasks:
            if task.task_id == task_id:
                task_was_found = True
            else:
                remaining_tasks.append(task)
            
        if not task_was_found:
            raise TaskNotFoundError(
                    f"Task with ID {task_id} was not found."
                )
        
        self._save_all(remaining_tasks)
    
    def _save_all(self, tasks: list[Task]) -> None:
        """Saves a list of Tasks objects into a JSON file."""
        tasks_data = []
        
        for task in tasks:
            tasks_data.append(task.to_dict())
            
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(tasks_data, file, indent=4)
            
        except OSError as error:
            raise TaskStorageError("Tasks could not be saved.") from error
        
# SERVICE LAYER
class TaskService:
    """Service Layer/ Uses cases:
    
    Coordinates busisness operations for tasks:
        - create task
        - list task by ID
        - list task by status
        - find task
        - update task description
        - update task details
        - delete task 

    Punto clave: TaskService depende de TaskRepository.
    """
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository
        
    def add_task(
        self,
        task_id: int, 
        title: str,
        description: str, 
        status: str 
    ) -> Task:
        task = Task(
        task_id=task_id,
        title=title,
        description=description,
        status=status
        )
        self._repository.add(task)
        
        return task
        
    def list_tasks(self) -> list[Task]:
        return self._repository.list_all()
    
    def find_task_by_id(self, task_id: int) -> Task:
        return self._repository.get_by_id(task_id)
    
    def list_tasks_by_status(self, status: str) -> list[Task]:
        return self._repository.list_by_status(status)
    
    def rename_task(self, task_id:int, new_name:str) -> Task:
        task = self._repository.get_by_id(task_id)
        task.rename(new_name)
        self._repository.update(task)
        
        return task
    
    def update_task_status(self, task_id: int, new_status: str) -> Task:
        task = self._repository.get_by_id(task_id)
        task.update_status(new_status)
        self._repository.update(task)

        return task
    
    def update_task_description(self, task_id: int, new_description:str) -> Task:
        task = self._repository.get_by_id(task_id)
        task.update_description(new_description)
        self._repository.update(task)
        
        return task
    
    def update_details(self, task_id: int, new_title:str, new_description:str) -> Task:
        task = self._repository.get_by_id(task_id)
        task.rename(new_title)
        task.update_description(new_description)
        self._repository.update(task)
        
        return task
    
    def delete_task(self, task_id: int) -> None:
        self._repository.delete(task_id)
        
        
# INTERFACE
def show_menu() -> None:
    print("\n=== TASKS MANAGER SYSTEM (V5) ===")
    print("1. Add task.")
    print("2. List tasks.")
    print("3. Finds task by ID.")
    print("4. Filter tasks by status.")
    print("5. Update task status.")
    print("6. Rename task.")
    print("7. Update task description.")
    print("8. Update task details")
    print("9. Delete task.")
    print("0. Exit.")
    
def ask_option() -> str:
    while True:
        option = input("Choose an option: ".strip())
        
        if option in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
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
    """Composition root.
    
    Aquí se decide que implementación concreta usar.
    
    Para consola real:
        JSONTaskRepository
    Para tests:
        InMemoryTaskRepository
    """
    repository = JSONTaskRepository("task_data.json")
    service = TaskService(repository)
    
    while True:
        show_menu()
        option = ask_option()
        
        if option == "0":
            print("Exiting task manager system.")
            break
        
        elif option == "1":
            try:
                task_id = ask_positive_int("Task ID: ")
                title = ask_non_empty_text("Title: ")
                description = ask_non_empty_text("Description: ")
                status = ask_non_empty_text("Status: ")
                
                service.add_task(
                    task_id=task_id, 
                    title=title,
                    description=description, 
                    status=status
                )
                print("Task added successfully.")
                
            except TaskAlreadyExistsError as error:
                print(error)
            
            except InvalidTaskStatusError as error:
                print(error)
            
            except(TypeError) as error:
                print(f"Invalid task data: {error}")

            except(ValueError) as error:
                print(f"Invalid task data: {error}")
                
        elif option == "2":
            try:
                tasks = service.list_tasks()
                print_tasks(tasks)
            
            except TaskStorageError as error:
                print(f"Storage error: {error}")
                
        elif option == "3":
            task_id = ask_positive_int("Task ID: ")
            
            try:
                task = service.find_task_by_id(task_id)
                print_task(task)
            
            except TaskNotFoundError as error:
                print(error)
            
            except TaskStorageError as error:
                print(f"Storage error: {error}")
        
        elif option == "4":
            task_status = ask_non_empty_text("Status: ")
            
            try:
                filtered_tasks = service.list_tasks_by_status(task_status)
                print_tasks(filtered_tasks)
                
            except InvalidTaskStatusError as error:
                print(error)
        
        elif option == "5":
            task_id = ask_positive_int("Task ID: ")
            new_status = ask_non_empty_text("New status: ")
            
            try:
                service.update_task_status(task_id, new_status)
                print("Status renamed successfully.")
            
            except TaskNotFoundError as error:
                print(error)
            
            except InvalidTaskStatusError as error:
                print(error)

            except(TypeError) as error:
                print(f"Invalid product data: {error}")
            
            except(ValueError) as error:
                print(f"Invalid product data: {error}")
        
        elif option == "6":
            task_id = ask_positive_int("Task ID: ")
            new_title = ask_non_empty_text("New title: ")
            
            try:
                service.rename_task(task_id, new_title)
                print("New title updated successfully.")
            
            except TaskNotFoundError as error:
                print(error)
            
            except(TypeError) as error:
                print(f"Invalid task data: {error}")
                
            except(ValueError) as error:
                print(f"Invalid task data: {error}")
        
        elif option == "7":
            task_id = ask_positive_int("Task ID: ")
            new_description = ask_non_empty_text("New description: ")
            
            try:
                service.update_task_description(task_id, new_description)
                print("Task description updated sucessfully.")
            
            except TaskNotFoundError as error:
                print(error)
            
            except(TypeError) as error:
                print(f"Invalid task data: {error}")
            
            except(ValueError) as error:
                print(f"Invalid task data: {error}")
        
        elif option == "8":
            task_id = ask_positive_int("Task ID: ")
            new_title = ask_non_empty_text("New title: ")
            new_description = ask_non_empty_text("New description: ")
            
            try:
                service.update_details(task_id, new_title, new_description)
                print("Task content updated sucessfully.")
            
            except TaskNotFoundError as error:
                print(error)
                
            except(TypeError) as error:
                print(f"Invalid task data: {error}")
            
            except(ValueError) as error:
                print(f"Invalid task data: {error}")
                
        elif option == "9":
            task_id = ask_positive_int("Task ID: ")
            
            try:
                service.delete_task(task_id)
                print("Task deleted successfully.")
            
            except TaskNotFoundError as error:
                print(error)

if __name__ == "__main__":
    main()