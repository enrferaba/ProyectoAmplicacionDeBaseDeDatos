-- Datos de ejemplo para poblar la base de datos.

INSERT INTO estudiantes (id, nombre, email, telefono, fecha_registro) VALUES
    (1, 'Ana López', 'ana.lopez@example.com', '+34 600 111 111', '2024-01-15'),
    (2, 'Bruno Díaz', 'bruno.diaz@example.com', '+34 600 222 222', '2024-02-10'),
    (3, 'Carla Pérez', 'carla.perez@example.com', '+34 600 333 333', '2024-02-12'),
    (4, 'Diego Ramos', 'diego.ramos@example.com', '+34 600 444 444', '2024-03-02');

INSERT INTO profesores (id, nombre, email) VALUES
    (1, 'Lucía Herrera', 'lucia.herrera@example.com'),
    (2, 'Miguel Ortega', 'miguel.ortega@example.com'),
    (3, 'Sofía Vega', 'sofia.vega@example.com');

INSERT INTO cursos (id, nombre, descripcion, profesor_id, cupo_maximo, fecha_inicio, fecha_fin) VALUES
    (1, 'SQL Básico', 'Aprende las sentencias esenciales de SQL.', 1, 25, '2024-09-01', '2024-10-15'),
    (2, 'Modelado de Datos', 'Taller práctico de diseño entidad-relación.', 2, 20, '2024-10-20', '2024-12-01'),
    (3, 'ETL con Python', 'Procesos de extracción, transformación y carga.', 3, 18, '2024-11-05', '2025-01-10');

INSERT INTO evaluaciones (id, curso_id, nombre, porcentaje, fecha_entrega) VALUES
    (1, 1, 'Práctica consultas', 30, '2024-09-20'),
    (2, 1, 'Proyecto final', 40, '2024-10-10'),
    (3, 1, 'Examen final', 30, '2024-10-15'),
    (4, 2, 'Caso de estudio', 40, '2024-11-15'),
    (5, 2, 'Proyecto de modelado', 60, '2024-11-30'),
    (6, 3, 'Pipeline ETL', 50, '2024-12-10'),
    (7, 3, 'Examen final', 50, '2025-01-10');

INSERT INTO matriculas (id, estudiante_id, curso_id, fecha_matricula, estado) VALUES
    (1, 1, 1, '2024-08-20', 'aprobada'),
    (2, 1, 2, '2024-10-18', 'aprobada'),
    (3, 2, 1, '2024-08-25', 'aprobada'),
    (4, 2, 3, '2024-11-02', 'activa'),
    (5, 3, 2, '2024-10-21', 'activa'),
    (6, 4, 1, '2024-09-03', 'retirada');

INSERT INTO calificaciones (id, matricula_id, evaluacion_id, nota, fecha_registro) VALUES
    (1, 1, 1, 8.5, '2024-09-21'),
    (2, 1, 2, 9.1, '2024-10-11'),
    (3, 1, 3, 8.9, '2024-10-16'),
    (4, 2, 4, 9.5, '2024-11-16'),
    (5, 2, 5, 9.8, '2024-12-01'),
    (6, 3, 1, 7.3, '2024-09-22'),
    (7, 3, 2, 7.8, '2024-10-11'),
    (8, 3, 3, 7.0, '2024-10-16');
