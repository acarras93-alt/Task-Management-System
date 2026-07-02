import pytest

from task_v5 import Task, InvalidTaskStatusError


def test_create_task_with_valid_data():
    """
    Problema:
    Necesitamos comprobar que una tarea válida puede existir en el sistema.

    Comprobación:
    Creamos una Task con datos correctos.

    Solución:
    Si la entidad se construye correctamente, sus atributos deben conservar
    los valores esperados.
    """
    task = Task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    assert task.task_id == 1
    assert task.title == "Study pytest"
    assert task.description == "Create basic backend tests"
    assert task.status == "pending"


def test_task_title_cannot_be_empty():
    """
    Problema:
    Una tarea sin título no tiene sentido de negocio.

    Comprobación:
    Intentamos crear una Task con un título vacío.

    Solución:
    El dominio debe rechazarla lanzando ValueError.
    """
    with pytest.raises(ValueError):
        Task(
            task_id=1,
            title="   ",
            description="Valid description",
            status="pending",
        )


def test_task_description_cannot_be_empty():
    """
    Problema:
    Una tarea sin descripción pierde información mínima de contexto.

    Comprobación:
    Intentamos crear una Task con descripción vacía.

    Solución:
    El dominio debe rechazarla lanzando ValueError.
    """
    with pytest.raises(ValueError):
        Task(
            task_id=1,
            title="Valid title",
            description="   ",
            status="pending",
        )


def test_task_id_must_be_zero_or_greater():
    """
    Problema:
    Un ID negativo no representa correctamente una identidad de entidad.

    Comprobación:
    Intentamos crear una Task con task_id negativo.

    Solución:
    El dominio debe rechazarla lanzando ValueError.
    """
    with pytest.raises(ValueError):
        Task(
            task_id=-1,
            title="Valid title",
            description="Valid description",
            status="pending",
        )


def test_task_status_must_be_valid():
    """
    Problema:
    El negocio solo permite estados controlados.

    Comprobación:
    Intentamos crear una Task con un estado no permitido.

    Solución:
    El dominio debe lanzar InvalidTaskStatusError.
    """
    with pytest.raises(InvalidTaskStatusError):
        Task(
            task_id=1,
            title="Valid title",
            description="Valid description",
            status="blocked",
        )


def test_task_can_update_status():
    """
    Problema:
    Una tarea debe poder cambiar de estado dentro del flujo permitido.

    Comprobación:
    Creamos una tarea pending y la pasamos a completed.

    Solución:
    El estado final debe quedar actualizado.
    """
    task = Task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    task.update_status("completed")

    assert task.status == "completed"


def test_task_to_dict_and_from_dict_keep_domain_rules():
    """
    Problema:
    El sistema necesita guardar y reconstruir tareas desde datos serializados.

    Comprobación:
    Convertimos una Task a dict y la reconstruimos con from_dict.

    Solución:
    La tarea reconstruida debe mantener los mismos datos y seguir pasando
    por las validaciones del dominio.
    """
    task = Task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    task_data = task.to_dict()
    restored_task = Task.from_dict(task_data)

    assert restored_task.task_id == task.task_id
    assert restored_task.title == task.title
    assert restored_task.description == task.description
    assert restored_task.status == task.status