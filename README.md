# Task Management System V5
1. Problema que resuelve

Task Manager es una aplicación de consola desarrollada en Python para gestionar tareas de forma estructurada.

El sistema permite crear, listar, buscar, filtrar, actualizar y eliminar tareas. Cada tarea tiene un idenficador único, un título, una descrioción y un estado.

Este proyecto simula un pequeño sistema baackend donde se trabaja con entidades, reglas de negocio, capa de servicio, persistencia en JSON y tests automatizados.

El objetivo principal no es solo crear un programa que funciona, sino practicar una arquitectura clara, mantenible y cercana a la forma de trabajar en proyectos backend reales.

2. Arquitectura usada
El proyecto sigue una arquitectura por capas:
INTERFAZ / CONSOLA
↓
ORQUESTACIÓN
↓
CAPA DE SERVICIO
↓
CAPA DE DOMINIO
↓
CAPA DE PERSISTENCIA

Cada capa tiene una responsabilidad concreta:
-  La interfaz se encarga de pedir datos al usuario y mostrar resultados.
- La orquestación coordina el flujo principal del programa.
- La capa servicio gestiona los casos de uso.
- La capa dominio protege las reglas internas de la entidad Task.
- La capa de persistencia guarda y carga datos usando un archivo JSON.

Esta separación permite que el código sea más facil de  mantener, probar y entender.

3. Diferencia entre queries y commands
En este proyecto se distingue entre operaciones de consulta y operaciones de modificación. 
Queries: Las queries consultan informaición, pero no modifican el estado del sistema. Estas operaciones deben devolver información correcta sin alterar las tareas almacenadas. Ejemplos:
list_tasks()
find_task_by_id()
list_tasks_by_status()

Commands: Los commands modifican el estado del sistema. Estas operaciones deben cambiar el estado interno del sistema o lanzar una excepción clara si la operación no es válida. Ejemplos:
add_task()
update_task_status()
rename_task()
update_task_description()
update_task_details()
delete_task()

4. Testing

En la versión V5 se han añadido tests automatizados con pytest.

La estructura de tests es:
tests/
├── test_task.py
├── test_task_manager.py
└── test_task_repository.py

5. Aprendizajes principales

En esta versión he practicado los siguientes conceptos:

* Separación de responsabilidades por capas.
* Diferencia entre dominio, servicio, persistencia, interfaz y orquestación.
* Validaciones internas dentro de una entidad.
* Uso de excepciones específicas para errores de dominio, servicio y persistencia.
* Conversión entre objetos Python y datos JSON.
* Uso de to_dict y from_dict.
* Diferencia entre queries y commands.
* Creación de tests automatizados con pytest.
* Testing de entidades.
* Testing de casos de uso.
* Testing de persistencia con archivos temporales.
* Uso de tmp_path para evitar modificar archivos reales durante los tests.
* Mentalidad de backend orientada a comportamiento, no solo a que el código se ejecute.

6. Mejoras futuras

Posibles mejoras para próximas versiones:

* Inyectar el repositorio dentro de TaskManager para aplicar un Repository Pattern más limpio.
* Hacer que TaskManager coordine la persistencia internamente.
* Añadir rollback si ocurre un error al guardar después de una operación.
* Añadir opción de cancelar operaciones desde la interfaz.
* Separar el proyecto en varios módulos.
* Añadir más implementaciones de repositorio.
* Añadir tests para errores de escritura y lectura de archivos.
* Añadir integración continua con GitHub Actions.
* Preparar una futura versión API con FastAPI o Django REST Framework.

7. Estado final de la versión

Task Manager V5 queda cerrada con:
Dominio probado
Servicio probado
Repositorio probado
README documentado
25 tests passing




