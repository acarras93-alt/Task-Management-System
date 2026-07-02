import pytest

from task_v5 import (
    InMemoryTaskRepository,
    InvalidTaskStatusError,
    TaskAlreadyExistsError,
    TaskNotFoundError,
    TaskService,
)


def create_service() -> TaskService:
    """
    Helper de test.

    Problema:
    Cada test necesita un servicio limpio y aislado.

    Comprobación:
    Creamos un repositorio en memoria nuevo para cada test.

    Solución:
    Devolvemos un TaskService conectado a InMemoryTaskRepository.
    """
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    return service


def test_service_add_task_creates_and_stores_task():
    """
    Problema:
    El caso de uso principal es crear una tarea y guardarla.

    Comprobación:
    Añadimos una tarea mediante el servicio y luego la buscamos por ID.

    Solución:
    La tarea debe existir en el repositorio y conservar sus datos.
    """
    service = create_service()

    task = service.add_task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    stored_task = service.find_task_by_id(1)

    assert task.task_id == 1
    assert stored_task.title == "Study pytest"
    assert stored_task.status == "pending"


def test_service_does_not_allow_duplicate_task_id():
    """
    Problema:
    Dos tareas no pueden compartir el mismo ID.

    Comprobación:
    Creamos una tarea y luego intentamos crear otra con el mismo task_id.

    Solución:
    El sistema debe lanzar TaskAlreadyExistsError.
    """
    service = create_service()

    service.add_task(
        task_id=1,
        title="First task",
        description="First description",
        status="pending",
    )

    with pytest.raises(TaskAlreadyExistsError):
        service.add_task(
            task_id=1,
            title="Duplicated task",
            description="Duplicated description",
            status="pending",
        )


def test_service_finds_task_by_id():
    """
    Problema:
    El usuario necesita recuperar una tarea concreta.

    Comprobación:
    Creamos una tarea y la buscamos por su ID.

    Solución:
    El servicio debe devolver la tarea correcta.
    """
    service = create_service()

    service.add_task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    task = service.find_task_by_id(1)

    assert task.task_id == 1
    assert task.title == "Study pytest"


def test_service_raises_error_when_task_does_not_exist():
    """
    Problema:
    Buscar una tarea inexistente no debe devolver None silenciosamente.

    Comprobación:
    Intentamos buscar un ID que no existe.

    Solución:
    El servicio debe propagar TaskNotFoundError.
    """
    service = create_service()

    with pytest.raises(TaskNotFoundError):
        service.find_task_by_id(999)


def test_service_updates_task_status():
    """
    Problema:
    Una tarea debe poder avanzar en su flujo de estado.

    Comprobación:
    Creamos una tarea pending y la actualizamos a completed.

    Solución:
    El servicio debe devolver y persistir la tarea actualizada.
    """
    service = create_service()

    service.add_task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    updated_task = service.update_task_status(1, "completed")

    assert updated_task.status == "completed"
    assert service.find_task_by_id(1).status == "completed"


def test_service_rejects_invalid_status_update():
    """
    Problema:
    El servicio no debe permitir estados fuera del vocabulario del dominio.

    Comprobación:
    Intentamos actualizar una tarea a un estado no permitido.

    Solución:
    El dominio debe lanzar InvalidTaskStatusError a través del servicio.
    """
    service = create_service()

    service.add_task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    with pytest.raises(InvalidTaskStatusError):
        service.update_task_status(1, "blocked")


def test_service_filters_tasks_by_status():
    """
    Problema:
    El usuario necesita listar tareas por estado.

    Comprobación:
    Creamos varias tareas con diferentes estados y filtramos por pending.

    Solución:
    El servicio debe devolver solo las tareas con status pending.
    """
    service = create_service()

    service.add_task(1, "Task one", "Description one", "pending")
    service.add_task(2, "Task two", "Description two", "completed")
    service.add_task(3, "Task three", "Description three", "pending")

    pending_tasks = service.list_tasks_by_status("pending")

    assert len(pending_tasks) == 2

    for task in pending_tasks:
        assert task.status == "pending"


def test_service_deletes_task():
    """
    Problema:
    Una tarea debe poder eliminarse del sistema.

    Comprobación:
    Creamos una tarea, la eliminamos y luego intentamos buscarla.

    Solución:
    Después del borrado, buscarla debe lanzar TaskNotFoundError.
    """
    service = create_service()

    service.add_task(
        task_id=1,
        title="Study pytest",
        description="Create basic backend tests",
        status="pending",
    )

    service.delete_task(1)

    with pytest.raises(TaskNotFoundError):
        service.find_task_by_id(1)