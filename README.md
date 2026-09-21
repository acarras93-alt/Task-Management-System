# Task Manager System V5

Gestor de tareas por consola: permite crear, consultar, editar, filtrar por estado
y eliminar tareas, con persistencia JSON y pruebas automatizadas.

Proyecto de aprendizaje de backend. **El punto de entrada actual es
`task_v5.py`**; las versiones anteriores se conservan para mostrar la evolución.
No requiere dependencias externas para ejecutar la aplicación. La última
revisión local de las pruebas, el 21 de septiembre de 2026, obtuvo **40 tests
correctos con Python 3.14.0**.

## 1. Descripción del proyecto

Task Manager System es una aplicación backend de consola desarrollada en Python, revisada localmente con Python 3.14.0.

El objetivo del proyecto es gestionar tareas mediante una arquitectura backend separada por responsabilidades, aplicando conceptos fundamentales de desarrollo profesional:

- Entidad de dominio
- Capa de servicio
- Repositorio abstracto
- Persistencia intercambiable
- Manejo de excepciones
- Tests automatizados con pytest

Esta versión forma parte de un entrenamiento backend orientado a construir una base sólida para proyectos más avanzados con Django, FastAPI y APIs REST.

---

## 2. Objetivo de la versión V5

El objetivo principal de la versión V5 es añadir una capa básica de testing para proteger:

- Reglas de dominio de la entidad `Task`
- Casos de uso principales del servicio
- Errores esperados del sistema
- Comportamiento del repositorio en memoria
- Persistencia básica mediante JSON

La finalidad no es testear todo de forma indiscriminada, sino proteger las partes del sistema que representan comportamiento real de backend.

---

## 3. Arquitectura del sistema

El proyecto sigue una arquitectura backend separada por capas:

```text
Consola → TaskService → TaskRepository (contrato)
                             ↑
                    implementado por
                ┌────────────┴─────────────┐
       InMemoryTaskRepository    JSONTaskRepository
```

### 3.1 Domain

La capa de dominio contiene la entidad principal del sistema:

```text
Task
```

La entidad `Task` representa una tarea dentro del sistema y protege sus propias reglas internas.

Responsabilidades principales:

- Validar `task_id`
- Validar `title`
- Validar `description`
- Validar `status`
- Permitir cambios de estado válidos
- Convertir la entidad a diccionario
- Reconstruir la entidad desde diccionario

---

### 3.2 Service

La capa de servicio contiene los casos de uso principales del sistema.

```text
TaskService
```

Responsabilidades principales:

- Crear tareas
- Listar tareas
- Buscar tareas por ID
- Actualizar estado
- Actualizar detalles
- Eliminar tareas
- Filtrar tareas por estado

El servicio no conoce los detalles de persistencia. Trabaja contra una abstracción de repositorio.

---

### 3.3 Repository Pattern

El sistema usa Repository Pattern para desacoplar la lógica de negocio de la forma en la que se guardan los datos.

Contrato principal:

```text
TaskRepository
```

Implementaciones:

```text
InMemoryTaskRepository
JSONTaskRepository
```

Esto permite cambiar la persistencia sin modificar la lógica del servicio.

---

### 3.4 Console Interface

La interfaz de consola permite al usuario interactuar con el sistema mediante un menú.

La consola no contiene reglas de negocio. Su responsabilidad es recibir datos del usuario, llamar al servicio y mostrar resultados.

---

## 4. Entidad principal: Task

La entidad `Task` contiene los siguientes campos:

```text
task_id: int
title: str
description: str
status: str
```

Estados permitidos:

```text
pending
in_progress
completed
```

Una tarea válida debe cumplir las siguientes reglas:

- El `task_id` debe ser un número entero mayor o igual que cero.
- El `title` no puede estar vacío.
- La `description` no puede estar vacía.
- El `status` debe pertenecer a los estados permitidos.

Estas reglas pertenecen al dominio porque definen cuándo una tarea puede existir correctamente dentro del sistema.

---

## 5. Excepciones del sistema

El proyecto define excepciones específicas para representar errores controlados:

```text
TaskAlreadyExistsError
TaskNotFoundError
InvalidTaskStatusError
TasksStorageError
```

Estas excepciones evitan que el sistema devuelva errores ambiguos o valores silenciosos como `None` cuando una operación no puede completarse correctamente.

Ejemplo:

```text
Si se busca una tarea inexistente, el sistema lanza TaskNotFoundError.
```

Esto hace que el comportamiento sea explícito, controlado y más fácil de testear.

---

## 6. Testing con pytest

La versión V5 añade tests automatizados usando `pytest`.

Los tests están organizados para proteger dos bloques principales:

```text
tests/test_task_domain.py
tests/test_task_service.py
```

Además, `tests/test_task.py`, `tests/test_task_manager.py` y
`tests/test_task_repository.py` prueban la versión V4, incluida su persistencia
JSON. El resultado conjunto de 40 tests incluye ambas versiones; no significa
que el repositorio JSON de V5 tenga esa misma cobertura.

---

## 7. Criterio de testing

El criterio usado para los tests es:

```text
No testear código por testear.
Testear reglas de dominio y casos de uso principales.
```

La IA puede ayudar a detectar escenarios posibles, pero la decisión final sobre qué tests mantener, descartar o aplazar pertenece al programador.

Cada test debe responder a una pregunta clara:

```text
¿Este test protege una regla real del dominio?
¿Este test protege una acción importante del sistema?
¿Este test protege un fallo que el sistema debe controlar?
```

---

## 8. Tests de dominio

Los tests de dominio protegen la validez interna de la entidad `Task`.

Pregunta principal:

```text
¿Puede existir esta entidad con estos datos?
```

Casos protegidos:

- Crear una tarea válida
- Rechazar título vacío
- Rechazar descripción vacía
- Rechazar `task_id` inválido
- Rechazar estado no permitido
- Permitir cambio de estado válido
- Convertir una tarea a diccionario
- Reconstruir una tarea desde diccionario

Ejemplo de criterio:

```text
Una Task sin título no representa una tarea válida dentro del sistema.
Por tanto, el dominio debe rechazarla.
```

---

## 9. Tests de servicio

Los tests de servicio protegen los casos de uso principales del sistema.

Pregunta principal:

```text
¿Puede el sistema ejecutar correctamente esta acción?
```

Casos protegidos:

- Crear una tarea
- Evitar tareas duplicadas
- Buscar tarea por ID
- Controlar búsqueda de tarea inexistente
- Actualizar estado
- Rechazar estado inválido
- Filtrar tareas por estado
- Eliminar tareas

Ejemplo de criterio:

```text
Actualizar el estado de una tarea protege una acción real del usuario.
Buscar una tarea inexistente protege un fallo que el sistema debe controlar.
```

---

## 10. Uso de repositorio en memoria para tests

Los tests de servicio usan `InMemoryTaskRepository`.

Motivo:

```text
El objetivo es testear la lógica del servicio sin depender de archivos JSON,
rutas del sistema operativo o estado externo.
```

Esto permite que los tests sean:

- Rápidos
- Aislados
- Repetibles
- Independientes de infraestructura

Defensa técnica:

```text
TaskService depende de TaskRepository, no de una implementación concreta.
Por eso puedo usar InMemoryTaskRepository en tests y JSONTaskRepository en ejecución real.
```

---

## 11. Ejecución del proyecto

Desde la raíz del proyecto, en macOS o Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install pytest ruff
python task_v5.py
```

En Windows, activa el entorno con `.venv\Scripts\Activate.ps1` desde PowerShell.
pytest y Ruff son herramientas de desarrollo. Los datos se guardan en
`task_data.json`, relativo al directorio desde el que se ejecuta el programa.

---

## 12. Ejecución de tests

Para ejecutar toda la batería de tests:

```bash
python3 -m pytest -q
```

Resultado de la revisión local del 21 de septiembre de 2026:

```text
40 passed
```

También se pueden ejecutar tests específicos:

```bash
python3 -m pytest tests/test_task_domain.py -q
```

```bash
python3 -m pytest tests/test_task_service.py -q
```

---

## 13. Resultado actual

Resultado de la suite completa en la revisión indicada:

```text
40 tests passed
```

Los tests existentes comprueban, dentro de su alcance:

- Las reglas principales del dominio están protegidas.
- Los casos de uso principales del servicio están protegidos.
- Los errores esperados están controlados.
- El sistema tiene una base de testing defendible para portfolio backend.

---

Para comprobar la calidad estática de la versión actual y las pruebas:

```bash
python -m ruff check task_v5.py tests
```

## 14. Decisiones técnicas defendibles

### Separación por capas

El sistema separa dominio, servicio, repositorio e interfaz de consola.

Esto evita mezclar reglas de negocio con entrada/salida de usuario o persistencia.

---

### Repository Pattern

El servicio no depende directamente de JSON.

Depende de una abstracción:

```text
TaskRepository
```

Esto permite cambiar la persistencia sin modificar los casos de uso.

---

### Excepciones específicas

El sistema usa excepciones propias para representar errores del dominio y del servicio.

Esto mejora la claridad del flujo y evita errores silenciosos.

---

### Tests con repositorio en memoria

Los tests de servicio usan una implementación en memoria para aislar la lógica de negocio.

Esto permite comprobar los casos de uso sin depender de infraestructura externa.

---

## 15. Qué no se prioriza en esta versión

En esta versión no se priorizan tests de la interfaz de consola.

Motivo:

```text
La consola depende de input() y print().
Es testeable, pero aporta menos valor en esta fase que proteger dominio,
servicio y persistencia.
```

Prioridad actual:

```text
1. Domain tests
2. Service tests
3. Repository tests
4. JSON persistence tests
5. Console tests
```

---

## 16. Conclusión

Task Manager System V5 representa una evolución desde un CRUD básico hacia una arquitectura backend más profesional.

El sistema ya no depende de una única implementación de almacenamiento y cuenta con tests automatizados para proteger reglas de dominio y casos de uso principales.

Esta versión es defendible como proyecto de entrenamiento backend porque demuestra:

- Modelado de entidad
- Validaciones de dominio
- Separación por capas
- Repository Pattern
- Persistencia intercambiable
- Manejo de errores
- Testing automatizado
- Criterio técnico sobre qué merece ser testeado

---

## 17. Frase resumen para entrevista

```text
En esta versión he construido un Task Manager con arquitectura backend separada por capas.
La entidad Task protege sus propias reglas de dominio, el servicio coordina los casos de uso y la persistencia se desacopla mediante Repository Pattern.
Para la versión V5 añadí tests con pytest, usando repositorio en memoria para validar el servicio de forma rápida y aislada.
El criterio de testing fue proteger reglas reales del dominio, acciones principales del sistema y errores que el backend debe controlar.
```