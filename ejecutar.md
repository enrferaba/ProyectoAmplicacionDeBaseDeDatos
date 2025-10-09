# Guía rápida de ejecución (`ejecutar.md`)

Este archivo recoge los comandos básicos para trabajar con el proyecto final sin perderte. Ejecuta todo desde la carpeta raíz del repositorio.

## 1. Preparar la base de datos desde cero

```bash
python3 main.py --init-only
```

- Recrea todas las tablas.
- Carga los datos de ejemplo (puedes añadir `--sin-datos` para dejarla vacía).

## 2. Pipeline completo recomendado para revisar la entrega

```bash
python3 main.py
```

Acciones que realiza automáticamente:

1. Reinicia la base con los datos de ejemplo.
2. Ejecuta las consultas guardadas mostrando el SQL en pantalla.
3. Genera los reportes CSV en `data/reportes/`.
4. Lanza la checklist de requisitos del proyecto.

## 3. Comandos útiles según la tarea

### Mostrar únicamente las consultas

```bash
python3 main.py --consultas
```

*(Añade `--reiniciar` si quieres garantizar que trabajas con datos recién cargados).* 

### Generar reportes sin mostrar nada por pantalla

```bash
python3 main.py --exportar-reportes
```

*(Recomendado acompañarlo de `--reiniciar` para empezar limpio).* 

### Verificar que todo cumple los requisitos

```bash
python3 main.py --check
```

### Lanzar el menú interactivo

```bash
python3 main.py --menu
```

Opciones disponibles en el menú:

1. Listar estudiantes, cursos y nota media.
2. Registrar un nuevo estudiante.
3. Matricular a un estudiante en un curso.
4. Registrar una nota (recalcula el estado automáticamente).
5. Generar reportes en CSV.

> Consejo: si necesitas una base limpia antes del menú, ejecuta `python3 main.py --reiniciar --menu`.

## 4. Limpieza de reportes

Los CSV se guardan dentro de `data/reportes/`. Puedes borrarlos manualmente o regenerarlos con `python3 main.py --exportar-reportes` cuando los necesites.
