-- Proyecto final de Ampliación de Bases de Datos
-- Archivo: schema.sql
-- Descripción: creación de tablas para una base de datos simple de cursos.

DROP TABLE IF EXISTS estudiantes;
DROP TABLE IF EXISTS cursos;
DROP TABLE IF EXISTS matriculas;

CREATE TABLE estudiantes (
    estudiante_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cursos (
    curso_id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    fecha_inicio TEXT,
    fecha_fin TEXT
);

CREATE TABLE matriculas (
    matricula_id INTEGER PRIMARY KEY,
    estudiante_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha_matricula TEXT DEFAULT CURRENT_TIMESTAMP,
    nota REAL,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(estudiante_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(curso_id)
);
