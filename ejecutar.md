# Guía rápida para ejecutar el proyecto

Esta chuleta recoge todos los comandos que utilicé para preparar y probar el proyecto.
La idea es que puedas copiarlos uno a uno en la terminal sin miedo a perderte.

## 1. Comprobar versión de Python
Asegúrate de que tienes Python instalado (versión 3.8 o superior):

```bash
python3 --version
```

## 2. Crear un entorno virtual (opcional pero recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
```

## 3. Ejecutar el script principal

```bash
python3 main.py
```

Este comando creará la base de datos en `data/academico.db` y mostrará los resultados de las
consultas de ejemplo directamente en la terminal.

## 4. Inspeccionar la base de datos (opcional)
Si quieres revisar el contenido manualmente, puedes abrir una sesión interactiva de SQLite:

```bash
sqlite3 data/academico.db
```

Dentro de la consola de SQLite puedes usar comandos como:

```sql
.tables
SELECT * FROM estudiantes;
SELECT * FROM cursos;
SELECT * FROM matriculas;
```

Cuando termines, sal de la consola escribiendo:

```sql
.exit
```

## 5. Repetir el proceso desde cero
Si cambiaste algo en los archivos de SQL, vuelve a ejecutar:

```bash
python3 main.py
```

El script borra y recrea las tablas, así que siempre tendrás la versión más reciente de tus datos.
