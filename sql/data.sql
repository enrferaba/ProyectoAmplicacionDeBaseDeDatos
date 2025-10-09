-- Datos de ejemplo para poblar la base de datos.

INSERT INTO estudiantes (estudiante_id, nombre, email) VALUES
(1, 'Ana López', 'ana.lopez@example.com'),
(2, 'Bruno Díaz', 'bruno.diaz@example.com'),
(3, 'Carla Pérez', 'carla.perez@example.com');

INSERT INTO cursos (curso_id, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(1, 'SQL Básico', 'Aprender consultas básicas.', '2024-09-01', '2024-10-15'),
(2, 'Modelado de Datos', 'Fundamentos de diseño de bases de datos.', '2024-10-20', '2024-12-01'),
(3, 'ETL con Python', 'Práctica con extracción y carga.', '2024-11-05', '2025-01-10');

INSERT INTO matriculas (matricula_id, estudiante_id, curso_id, fecha_matricula, nota) VALUES
(1, 1, 1, '2024-08-20', 8.5),
(2, 1, 2, '2024-10-18', 9.1),
(3, 2, 1, '2024-08-25', 7.3),
(4, 3, 2, '2024-10-21', NULL);
