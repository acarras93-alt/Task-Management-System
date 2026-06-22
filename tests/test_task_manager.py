import pytest

from task_v4 import (
    Task,
    TaskManager,
    TaskAlreadyExistsError,
    TaskNotFoundError,
    InvalidTaskStatusError
)


def create_task(task_id: int = 1, status: str = "pending") -> Task:
    return Task(
        task_id=task_id,
        title="Study Python",
        description="Practice pytest basics",
        status=status
    )
    
    
    
# First service test
def test_add_task_stores_task_in_manager():
    manager = TaskManager()
    task = create_task()

    manager.add_task(task)

    tasks = manager.list_tasks()

    assert len(tasks) == 1
    assert tasks[0] == task
    
def test_add_duplicated_task_id_raises_error():
    manager = TaskManager()
    task = create_task()
    duplicated_task = create_task()

    manager.add_task(task)

    with pytest.raises(TaskAlreadyExistsError):
        manager.add_task(duplicated_task)

def test_find_task_by_id_returns_correct_task():
    manager = TaskManager()
    task = create_task(task_id=1)

    manager.add_task(task)

    found_task = manager.find_task_by_id(1)

    assert found_task == task
    
def test_find_task_by_id_raises_error_when_task_does_not_exist():
    manager = TaskManager()

    with pytest.raises(TaskNotFoundError):
        manager.find_task_by_id(999)
        
# Query test: filter by status
def test_list_tasks_by_status_returns_only_matching_tasks():
    manager = TaskManager()

    task_1 = create_task(task_id=1, status="pending")
    task_2 = create_task(task_id=2, status="completed")
    task_3 = create_task(task_id=3, status="pending")

    manager.add_task(task_1)
    manager.add_task(task_2)
    manager.add_task(task_3)

    pending_tasks = manager.list_tasks_by_status("pending")

    assert len(pending_tasks) == 2
    assert task_1 in pending_tasks
    assert task_3 in pending_tasks
    assert task_2 not in pending_tasks
    
def test_list_tasks_by_invalid_status_raises_error():
    manager = TaskManager()

    with pytest.raises(InvalidTaskStatusError):
        manager.list_tasks_by_status("invalid")

# Comannd tests: update and delete
def test_update_task_status_changes_task_status():
    manager = TaskManager()
    task = create_task()

    manager.add_task(task)

    manager.update_task_status(1, "completed")

    updated_task = manager.find_task_by_id(1)

    assert updated_task.status == "completed"

def test_update_task_status_raises_error_when_task_does_not_exist():
    manager = TaskManager()

    with pytest.raises(TaskNotFoundError):
        manager.update_task_status(999, "completed")

def test_delete_task_removes_task_from_manager():
    manager = TaskManager()
    task = create_task()

    manager.add_task(task)

    manager.delete_task(1)

    assert manager.list_tasks() == []
    

def test_delete_task_raises_error_when_task_does_not_exist():
    manager = TaskManager()

    with pytest.raises(TaskNotFoundError):
        manager.delete_task(999)