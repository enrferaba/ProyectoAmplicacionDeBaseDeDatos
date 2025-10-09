-- Consultas de ejemplo para revisar la base de datos.

-- 1. Listar todos los estudiantes con sus cursos.
SELECT e.nombre AS estudiante, c.nombre AS curso, m.nota
FROM estudiantes e
JOIN matriculas m ON e.estudiante_id = m.estudiante_id
JOIN cursos c ON m.curso_id = c.curso_id
ORDER BY e.nombre;

-- 2. Contar cuántos estudiantes hay por curso.
SELECT c.nombre AS curso, COUNT(m.estudiante_id) AS total_estudiantes
FROM cursos c
LEFT JOIN matriculas m ON c.curso_id = m.curso_id
GROUP BY c.curso_id
ORDER BY total_estudiantes DESC;

-- 3. Mostrar estudiantes sin nota final.
SELECT e.nombre, c.nombre AS curso
FROM matriculas m
JOIN estudiantes e ON m.estudiante_id = e.estudiante_id
JOIN cursos c ON m.curso_id = c.curso_id
WHERE m.nota IS NULL;
