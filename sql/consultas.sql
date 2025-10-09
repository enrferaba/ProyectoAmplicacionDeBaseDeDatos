-- Consultas de ejemplo para revisar la base de datos.

-- 1. Promedio de notas por estudiante y curso.
SELECT
    e.nombre AS estudiante,
    c.nombre AS curso,
    ROUND(AVG(cal.nota), 2) AS nota_media,
    m.estado
FROM estudiantes e
JOIN matriculas m ON m.estudiante_id = e.id
JOIN cursos c ON c.id = m.curso_id
LEFT JOIN calificaciones cal ON cal.matricula_id = m.id
GROUP BY e.id, c.id
ORDER BY e.nombre, c.nombre;

-- 2. Ocupación de los cursos frente al cupo máximo.
SELECT
    c.nombre AS curso,
    SUM(CASE WHEN m.estado != 'retirada' THEN 1 ELSE 0 END) AS estudiantes_activos,
    c.cupo_maximo,
    ROUND(100.0 * SUM(CASE WHEN m.estado != 'retirada' THEN 1 ELSE 0 END) / c.cupo_maximo, 2) AS porcentaje_ocupacion
FROM cursos c
LEFT JOIN matriculas m ON m.curso_id = c.id
GROUP BY c.id
ORDER BY porcentaje_ocupacion DESC;

-- 3. Evaluaciones pendientes por estudiante.
SELECT
    e.nombre AS estudiante,
    c.nombre AS curso,
    ev.nombre AS evaluacion_pendiente,
    ev.fecha_entrega
FROM evaluaciones ev
JOIN cursos c ON c.id = ev.curso_id
JOIN matriculas m ON m.curso_id = c.id
JOIN estudiantes e ON e.id = m.estudiante_id
LEFT JOIN calificaciones cal ON cal.evaluacion_id = ev.id AND cal.matricula_id = m.id
WHERE cal.id IS NULL AND m.estado = 'activa'
ORDER BY ev.fecha_entrega;

-- 4. Agenda de cursos por profesor.
SELECT
    p.nombre AS profesor,
    c.nombre AS curso,
    DATE(c.fecha_inicio) AS fecha_inicio,
    DATE(c.fecha_fin) AS fecha_fin,
    SUM(CASE WHEN m.estado != 'retirada' THEN 1 ELSE 0 END) AS estudiantes_activos
FROM profesores p
JOIN cursos c ON c.profesor_id = p.id
LEFT JOIN matriculas m ON m.curso_id = c.id
GROUP BY p.id, c.id
ORDER BY p.nombre;

-- 5. Resumen de aprobaciones por estudiante.
SELECT
    e.nombre,
    SUM(CASE WHEN m.estado = 'aprobada' THEN 1 ELSE 0 END) AS cursos_aprobados,
    SUM(CASE WHEN m.estado = 'reprobada' THEN 1 ELSE 0 END) AS cursos_reprobados,
    SUM(CASE WHEN m.estado = 'activa' THEN 1 ELSE 0 END) AS cursos_en_progreso
FROM estudiantes e
LEFT JOIN matriculas m ON m.estudiante_id = e.id
GROUP BY e.id
ORDER BY e.nombre;
