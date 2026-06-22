import json

import pytest

from task_v4 import Task, TaskRepository, TasksStorageError

def create_task(task_id: int = 1, status: str = "pending") -> Task:
    return Task(
        task_id=task_id,
        title="Study Python",
        description="Practice pytest basics",
        status=status
    )

# Test: si el archivo no existe, devuelve lista vacia
def test_load_tasks_returns_empty_list_when_file_does_not_exist(tmp_path):
    file_path = tmp_path / "missing_tasks.json"
    repository = TaskRepository(file_path)

    tasks = repository.load_tasks()

    assert tasks == []

# Test: guardar tareas crea un archivo JSON
def test_save_tasks_creates_json_file(tmp_path):
    file_path = tmp_path / "tasks.json"
    repository = TaskRepository(file_path)
    task = create_task()

    repository.save_tasks([task])

    assert file_path.exists()

# Test: guardar tareas escribe datos correctos
def test_save_tasks_writes_task_data_to_json_file(tmp_path):
    file_path = tmp_path / "tasks.json"
    repository = TaskRepository(file_path)
    task = create_task()

    repository.save_tasks([task])

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [
        {
            "task_id": 1,
            "title": "Study Python",
            "description": "Practice pytest basics",
            "status": "pending"
        }
    ]
    
# Test: cargar tareas devuelve objetos Task
def test_load_tasks_returns_task_objects(tmp_path):
    file_path = tmp_path / "tasks.json"

    tasks_data = [
        {
            "task_id": 1,
            "title": "Study Python",
            "description": "Practice pytest basics",
            "status": "pending"
        }
    ]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tasks_data, file)

    repository = TaskRepository(file_path)

    tasks = repository.load_tasks()

    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert tasks[0].task_id == 1
    assert tasks[0].title == "Study Python"
    assert tasks[0].description == "Practice pytest basics"
    assert tasks[0].status == "pending"

# Test: JSON corrupto lanza TasksStorageError
def test_load_tasks_raises_storage_error_when_json_is_invalid(tmp_path):
    file_path = tmp_path / "tasks.json"

    with file_path.open("w", encoding="utf-8") as file:
        file.write("{ invalid json }")

    repository = TaskRepository(file_path)

    with pytest.raises(TasksStorageError):
        repository.load_tasks()