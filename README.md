# Proyecto de Ampliación de Bases de Datos (versión novata pero completa)

> Trabajo final desarrollado paso a paso, siguiendo los apuntes de clase y documentando
todo con detalle para que incluso alguien que empieza desde cero pueda reproducirlo.

## 1. Objetivo del proyecto

Construimos un sistema académico sencillo que cubre los elementos típicos exigidos en la asignatura:

- **Modelo relacional completo** con estudiantes, profesores, cursos, matrículas, evaluaciones y calificaciones.
- **Integridad referencial** mediante claves foráneas y restricciones `CHECK`.
- **Vista** para resumir la situación académica de cada estudiante.
- **Triggers** que impiden errores comunes (por ejemplo, que las evaluaciones superen el 100% del curso).
- **Consultas analíticas** listas para practicar joins, agregaciones y reporting.
- **Script en Python** que automatiza la creación de la base de datos, genera reportes y valida los requisitos.
- **Menú interactivo** para registrar nuevos estudiantes, matrículas y notas sin tocar SQL manualmente.

Todo está pensado para que puedas ejecutar el proyecto en tu propio ordenador, revisarlo con calma y adaptarlo a tu entrega final.

## 2. Estructura de carpetas

```
.
├── data/                  # Aquí se genera la base de datos y los reportes CSV
├── sql/
│   ├── schema.sql         # Definición completa del modelo relacional + triggers + vista
│   ├── data.sql           # Datos de ejemplo para arrancar rápidamente
│   └── consultas.sql      # Consultas de práctica y reporting
├── main.py                # Script principal con CLI y comprobaciones
├── ejecutar.md            # Chuleta con todos los comandos
└── README.md              # Este documento explicativo
```

## 3. Modelo de datos explicado como principiante

El dominio es una pequeña academia. El diagrama lógico (texto) sería:

```
Estudiantes (1) ───< Matriculas >─── (1) Cursos ───< Evaluaciones ───< Calificaciones
        │                              │
        └────────────── Prof. ────────┘
```

- `estudiantes`: datos básicos de la persona (nombre, email, teléfono).
- `profesores`: quién imparte cada curso.
- `cursos`: oferta académica con fechas y un cupo máximo.
- `matriculas`: relación N:M entre estudiantes y cursos con estado (`activa`, `aprobada`, etc.).
- `evaluaciones`: entregas, exámenes o proyectos ponderados hasta sumar el 100% del curso.
- `calificaciones`: notas que relacionan una matrícula concreta con una evaluación.
- `vw_resumen_estudiantes`: vista para mostrar nota media, porcentaje cubierto y estado final.

### Integridad que vigila la base de datos

- Claves foráneas con `ON DELETE CASCADE` para que, si borras un curso, desaparezcan sus matrículas y calificaciones asociadas.
- Restricciones `CHECK` para asegurar valores válidos (por ejemplo, notas entre 0 y 10).
- Triggers `trg_validar_porcentaje_insert/update` que evitan sumar más del 100% al definir evaluaciones.

## 4. Requisitos previos

- **Python 3.10 o superior** (se usa la sintaxis `list | None`).
- No necesitas instalar dependencias externas: todo usa la biblioteca estándar (`sqlite3`, `csv`, `argparse`).

## 5. Guía rápida para impacientes

1. Sitúate en la carpeta raíz del proyecto.
2. Ejecuta el flujo automático:

   ```bash
   python3 main.py
   ```

   El script recrea la base de datos, muestra las consultas, genera reportes CSV y valida que el proyecto cumpla los requisitos.

3. Abre la carpeta `data/` para encontrar `academico.db` y el directorio `reportes/` con los CSV.

Si quieres un desglose más minucioso, continúa leyendo :)

## 6. Explicación detallada de los scripts SQL

### 6.1 `sql/schema.sql`

- Activa `PRAGMA foreign_keys` y borra cualquier rastro previo (tablas, triggers, vista).
- Crea todas las tablas del modelo relacional con sus restricciones.
- Define la vista `vw_resumen_estudiantes` para ver la media, el porcentaje cubierto y el estado de cada matrícula.
- Incluye dos triggers que validan que la suma de `porcentaje` de las evaluaciones de un curso nunca supere el 100%.

### 6.2 `sql/data.sql`

- Añade cuatro estudiantes, tres profesores y tres cursos.
- Inserta evaluaciones que suman exactamente el 100% por curso.
- Registra seis matrículas en distintos estados para cubrir casos de uso (aprobada, activa, retirada).
- Carga calificaciones suficientes como para calcular medias realistas.

### 6.3 `sql/consultas.sql`

Cinco consultas listas para practicar:

1. **Promedio por estudiante y curso:** combina `JOIN` y `AVG`.
2. **Ocupación por curso:** compara número de matriculados vs. cupo máximo.
3. **Evaluaciones pendientes:** detecta entregas sin calificar.
4. **Agenda por profesor:** fechas clave y estudiantes activos por curso.
5. **Resumen de aprobaciones:** cuenta aprobadas, reprobadas y en progreso por estudiante.

## 7. Script principal `main.py`

El corazón del proyecto controla tres cosas:

1. **Automatización:** recrea la base de datos desde cero y ejecuta las consultas.
2. **Validaciones:** verifica tablas, vista, triggers, porcentajes y presencia de datos.
3. **Interacción:** ofrece un menú CLI para añadir estudiantes, matricularlos o registrar notas.

### 7.1 Uso por defecto

```
python3 main.py
```

Reinicia la base con los datos de ejemplo y ejecuta el pipeline completo:

- Muestra cada consulta con su SQL para que puedas aprender mientras observas los resultados.
- Exporta cada consulta a `data/reportes/reporte_XX.csv`.
- Lanza una checklist que confirma el cumplimiento de los requisitos del proyecto final.

### 7.2 Opciones disponibles

- `--init-only`: solo recrea la base de datos (ideal antes de pruebas manuales).
- `--sin-datos`: acompaña a `--init-only` o `--reiniciar` para crear la base vacía.
- `--reiniciar`: recrea la base antes de ejecutar otras acciones (por ejemplo, `--consultas`).
- `--consultas`: ejecuta y muestra las consultas guardadas.
- `--exportar-reportes`: genera/actualiza los CSV.
- `--check`: realiza las comprobaciones de requisitos.
- `--menu`: abre el menú interactivo para gestionar datos sin escribir SQL.

> **Ejemplo combinado:**
> ```bash
> python3 main.py --reiniciar --consultas --exportar-reportes --check
> ```
> Re-crea la base, muestra consultas, genera reportes y repasa la checklist.

### 7.3 Menú interactivo paso a paso

Al lanzar `python3 main.py --menu` podrás:

1. Ver el listado de estudiantes con sus cursos y nota media.
2. Registrar un nuevo estudiante (solo pide nombre y correo; el teléfono es opcional).
3. Matricular a alguien en un curso con el estado que prefieras.
4. Registrar calificaciones; el sistema recalcula automáticamente si la matrícula queda aprobada o reprobada cuando se completan todas las evaluaciones.
5. Generar reportes CSV en cualquier momento.

Cada opción valida los datos introducidos y muestra mensajes claros si algo falla (por ejemplo, un correo duplicado o un ID inexistente).

## 8. Validación del proyecto

La checklist que ejecuta `main.py` revisa:

- Que las tablas principales existan.
- Que la vista `vw_resumen_estudiantes` esté disponible.
- Que los triggers de control de porcentajes estén activos.
- Que cada curso tenga evaluaciones que sumen exactamente el 100%.
- Que haya un mínimo de datos de ejemplo (4 estudiantes, 3 cursos, 5 matrículas).

Si algún punto falla se muestra en pantalla con un mensaje para corregirlo.

## 9. Reportes generados

Cada consulta se exporta a un CSV dentro de `data/reportes/`. Esto es útil para adjuntar evidencias en la entrega o para practicar con hojas de cálculo.

- `reporte_01.csv`: promedio por estudiante y curso.
- `reporte_02.csv`: ocupación de cursos.
- `reporte_03.csv`: evaluaciones pendientes.
- `reporte_04.csv`: agenda docente.
- `reporte_05.csv`: resumen de aprobaciones.

## 10. Cómo seguir aprendiendo

- Añade más cursos o evaluaciones al `data.sql` y vuelve a ejecutar `python3 main.py`.
- Modifica las consultas o crea otras nuevas (por ejemplo, ranking de profesores según aprobaciones).
- Experimenta con `--sin-datos` para practicar entradas manuales desde el menú.
- Abre `data/academico.db` en DB Browser for SQLite y diseña nuevas vistas, índices o triggers.

## 11. Resolución de problemas comunes

| Problema | Posible causa | Solución |
|----------|---------------|----------|
| `sqlite3.OperationalError: no such table ...` | No se ejecutó `schema.sql` | Lanza `python3 main.py --reiniciar` |
| `IntegrityError: UNIQUE constraint failed` | Correo o matrícula duplicada | Revisa los IDs introducidos en el menú |
| Los reportes no aparecen | No se ejecutó `--exportar-reportes` | Usa `python3 main.py --exportar-reportes` |

## 12. Créditos

Proyecto elaborado por un estudiante motivado que siguió al pie de la letra los apuntes de clase, priorizando la claridad y la documentación para que cualquier novato pueda replicarlo.
