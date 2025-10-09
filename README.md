# Proyecto de Ampliación de Bases de Datos (versión novata)

> Este repositorio contiene mi intento completo de proyecto final para la asignatura. Lo hice
> repasando los apuntes de clase y con mentalidad de principiante: todo muy explicado, paso a paso
> y sin asumir que conozco trucos avanzados.

## 1. ¿De qué va el proyecto?

La idea es montar una base de datos académica muy sencilla para gestionar estudiantes, cursos y
matrículas. Usé **SQLite** porque es ligero, viene incluido con Python y no hay que instalar un
servidor aparte (ideal cuando todavía estoy aprendiendo).

El flujo básico es:

1. Crear las tablas principales (`estudiantes`, `cursos` y `matriculas`).
2. Cargar datos de ejemplo para poder practicar.
3. Ejecutar algunas consultas típicas que podrían salir en el examen o en ejercicios.

Todo esto se automatiza con un pequeño script en Python llamado `main.py`.

## 2. Estructura de carpetas

```
.
├── data/                # Aquí se guarda la base de datos generada (academico.db)
├── sql/                 # Archivos .sql con el esquema, los datos y consultas de ejemplo
├── main.py              # Script principal: crea la BD y lanza las consultas
├── ejecutar.md          # Chuleta con todos los comandos a ejecutar
└── README.md            # Este documento con la explicación completa
```

## 3. Archivos importantes

### 3.1 `sql/schema.sql`
Contiene las instrucciones para borrar tablas anteriores (si existen) y crearlas de nuevo con sus
respectivas columnas y claves primarias/foráneas. De esta forma puedo reiniciar el proyecto todas
las veces que haga falta sin preocuparme por errores de duplicados.

### 3.2 `sql/data.sql`
Rellena las tablas con datos realistas pero sencillos. Incluyo tres estudiantes, tres cursos y
cuatro matrículas para tener variedad (incluye el caso de una nota sin completar).

### 3.3 `sql/consultas.sql`
Guarda tres consultas pensadas para practicar joins y agregaciones:

1. Listar estudiantes con sus cursos y notas.
2. Contar cuántos estudiantes hay en cada curso.
3. Ver quiénes siguen sin nota final.

### 3.4 `main.py`
El script principal hace todo el trabajo:

1. Crea la carpeta `data/` si no existe.
2. Ejecuta `schema.sql` y `data.sql` para construir la base de datos desde cero.
3. Abre `consultas.sql` y ejecuta cada consulta imprimiendo los resultados en pantalla.

El código está lleno de mensajes por consola para saber qué está pasando. Intenté mantenerlo lo más
claro posible para que alguien sin mucha experiencia pueda seguir el flujo.

## 4. Requisitos

- Python 3.10 o superior (aunque debería funcionar desde Python 3.8 porque usa solo módulos de la
  biblioteca estándar).
- No necesitas instalar paquetes extra. `sqlite3` y `pathlib` vienen por defecto.

## 5. Pasos para ejecutar (resumen rápido)

1. Clonar o descargar este repositorio.
2. Abrir una terminal en la carpeta raíz del proyecto.
3. Ejecutar `python3 main.py` (más detalles en `ejecutar.md`).

El script generará el archivo `data/academico.db`. Si deseas abrirlo con un visor de bases de datos,
podrás reutilizarlo para tus propias consultas.

## 6. Resultados esperados

Al ejecutar el programa deberías ver algo parecido a esto en la terminal (puede variar el orden):

```
Iniciando creación de la base de datos...
Base de datos creada en: /ruta/al/proyecto/data/academico.db
Ejecutando consultas de ejemplo...

Resultado de la consulta 1:
  -  ('Ana López', 'SQL Básico', 8.5)
  -  ('Ana López', 'Modelado de Datos', 9.1)
  -  ('Bruno Díaz', 'SQL Básico', 7.3)
  -  ('Carla Pérez', 'Modelado de Datos', None)

Resultado de la consulta 2:
  -  ('SQL Básico', 2)
  -  ('Modelado de Datos', 2)
  -  ('ETL con Python', 0)

Resultado de la consulta 3:
  -  ('Carla Pérez', 'Modelado de Datos')

Proceso finalizado. Puedes revisar el archivo academico.db para más pruebas.
```

## 7. Cómo seguir aprendiendo

- Modifica `sql/data.sql` con más estudiantes o cursos y vuelve a ejecutar `python3 main.py` para
  ver cómo cambian los resultados.
- Añade nuevas consultas al final de `sql/consultas.sql` y comprueba qué sale en la terminal.
- Abre `data/academico.db` con un gestor como *DB Browser for SQLite* para practicar con interfaz
  gráfica.

## 8. Créditos

Proyecto creado por un estudiante motivado pero novato, basándome únicamente en los apuntes de
clase de la asignatura de Ampliación de Bases de Datos.
