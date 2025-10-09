-- Proyecto final de Ampliación de Bases de Datos
-- Archivo: schema.sql
-- Descripción: creación completa de la base de datos académica.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_resumen_estudiantes;
DROP TRIGGER IF EXISTS trg_validar_porcentaje_insert;
DROP TRIGGER IF EXISTS trg_validar_porcentaje_update;
DROP TABLE IF EXISTS calificaciones;
DROP TABLE IF EXISTS evaluaciones;
DROP TABLE IF EXISTS matriculas;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS profesores;
DROP TABLE IF EXISTS estudiantes;

CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT,
    fecha_registro TEXT DEFAULT (DATE('now'))
);

CREATE TABLE profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    profesor_id INTEGER NOT NULL,
    cupo_maximo INTEGER NOT NULL CHECK (cupo_maximo > 0),
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_matricula TEXT DEFAULT (DATE('now')),
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'retirada', 'aprobada', 'reprobada')),
    UNIQUE (estudiante_id, curso_id),
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE evaluaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    porcentaje REAL NOT NULL CHECK (porcentaje > 0 AND porcentaje <= 100),
    fecha_entrega TEXT,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
);

CREATE TABLE calificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula_id INTEGER NOT NULL,
    evaluacion_id INTEGER NOT NULL,
    nota REAL CHECK (nota >= 0 AND nota <= 10),
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (matricula_id, evaluacion_id),
    FOREIGN KEY (matricula_id) REFERENCES matriculas(id) ON DELETE CASCADE,
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(id) ON DELETE CASCADE
);

CREATE VIEW vw_resumen_estudiantes AS
SELECT
    e.id AS estudiante_id,
    e.nombre AS estudiante,
    e.email,
    c.nombre AS curso,
    ROUND(AVG(cal.nota), 2) AS nota_media,
    COALESCE(SUM(ev.porcentaje), 0) AS porcentaje_cubierto,
    m.estado
FROM estudiantes e
JOIN matriculas m ON m.estudiante_id = e.id
JOIN cursos c ON c.id = m.curso_id
LEFT JOIN calificaciones cal ON cal.matricula_id = m.id
LEFT JOIN evaluaciones ev ON ev.id = cal.evaluacion_id
GROUP BY e.id, c.id;

CREATE TRIGGER trg_validar_porcentaje_insert
BEFORE INSERT ON evaluaciones
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN (
                SELECT COALESCE(SUM(porcentaje), 0)
                FROM evaluaciones
                WHERE curso_id = NEW.curso_id
            ) + NEW.porcentaje > 100
            THEN RAISE(ABORT, 'La suma de porcentajes de evaluaciones supera el 100% para este curso')
        END;
END;

CREATE TRIGGER trg_validar_porcentaje_update
BEFORE UPDATE ON evaluaciones
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN (
                SELECT COALESCE(SUM(porcentaje), 0)
                FROM evaluaciones
                WHERE curso_id = NEW.curso_id AND id != OLD.id
            ) + NEW.porcentaje > 100
            THEN RAISE(ABORT, 'La suma de porcentajes de evaluaciones supera el 100% para este curso')
        END;
END;
