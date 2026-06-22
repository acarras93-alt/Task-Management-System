import pytest

from task_v4 import Task, InvalidTaskStatusError

def test_valid_task_creation():
    task = Task(
        task_id=1,
        title="Study Python",
        description="Practice pytest basics",
        status="pending"
    )

    assert task.task_id == 1
    assert task.title == "Study Python"
    assert task.description == "Practice pytest basics"
    assert task.status == "pending"
    

def test_empty_title_raises_value_error():
    with pytest.raises(ValueError):
        Task(
            task_id=1,
            title="",
            description="Practice pytest basics",
            status="pending"
        )
        
def test_empty_description_raises_value_error():
    with pytest.raises(ValueError):
        Task(
            task_id=1,
            title="Study Python",
            description="",
            status="pending"
        )
        
def test_invalid_status_raises_invalid_task_status_error():
    with pytest.raises(InvalidTaskStatusError):
        Task(
            task_id=1,
            title="Study Python",
            description="Practice pytest basics",
            status="wrong_status"
        )
        
def test_update_status_changes_task_status():
    task = Task(
        task_id=1,
        title="Study Python",
        description="Practice pytest basics",
        status="pending"
    )

    task.update_status("completed")

    assert task.status == "completed"
    
def test_update_status_rejects_invalid_status():
    task = Task(
        task_id=1,
        title="Study Python",
        description="Practice pytest basics",
        status="pending"
    )

    with pytest.raises(InvalidTaskStatusError):
        task.update_status("invalid")
        
def test_rename_changes_task_title():
    task = Task(
        task_id=1,
        title="Old title",
        description="Practice pytest basics",
        status="pending"
    )

    task.rename("New title")

    assert task.title == "New title"

def test_update_description_changes_task_description():
    task = Task(
        task_id=1,
        title="Study Python",
        description="Old description",
        status="pending"
    )

    task.update_description("New description")

    assert task.description == "New description"

def test_to_dict_returns_task_data_as_dictionary():
    task = Task(
        task_id=1,
        title="Study Python",
        description="Practice pytest basics",
        status="pending"
    )

    task_data = task.to_dict()

    assert task_data == {
        "task_id": 1,
        "title": "Study Python",
        "description": "Practice pytest basics",
        "status": "pending"
    }

def test_from_dict_creates_task_object():
    task_data = {
        "task_id": 1,
        "title": "Study Python",
        "description": "Practice pytest basics",
        "status": "pending"
    }

    task = Task.from_dict(task_data)

    assert isinstance(task, Task)
    assert task.task_id == 1
    assert task.title == "Study Python"
    assert task.description == "Practice pytest basics"
    assert task.status == "pending"