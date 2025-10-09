"""Proyecto completo de la asignatura de Ampliación de Bases de Datos.

El objetivo es ofrecer un ejemplo totalmente funcional pero escrito con mentalidad
novata: código claro, pasos guiados y muchas comprobaciones para asegurarnos de
que el proyecto final cumple todos los requisitos habituales (modelo relacional,
consultas avanzadas, triggers, vistas y utilidades de apoyo).
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reportes"
DATABASE_PATH = DATA_DIR / "academico.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
DATA_PATH = BASE_DIR / "sql" / "data.sql"
CONSULTAS_PATH = BASE_DIR / "sql" / "consultas.sql"


@dataclass
class QueryResult:
    """Representa el resultado de una consulta guardada en el proyecto."""

    sql: str
    headers: Sequence[str]
    rows: Sequence[Sequence[object]]


class DatabaseManager:
    """Gestiona todas las operaciones sobre la base de datos académica."""

    def __init__(self, db_path: Path = DATABASE_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conexion = sqlite3.connect(self.db_path)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion

    def initialize(self, with_sample_data: bool = True) -> None:
        """Recrea la base de datos desde cero con (o sin) datos de ejemplo."""
        print("-> Creando base de datos desde cero...")
        with self.connect() as conexion:
            self._run_script(conexion, SCHEMA_PATH)
            if with_sample_data:
                self._run_script(conexion, DATA_PATH)
            conexion.commit()
        print(f"-> Base de datos lista en {self.db_path}")

    def ensure_database(self) -> None:
        """Garantiza que la base de datos exista; si no, la crea con datos."""
        if not self.db_path.exists():
            print("No se encontró la base de datos. Se generará automáticamente con los datos de ejemplo...")
            self.initialize(with_sample_data=True)

    def run_saved_queries(self) -> List[QueryResult]:
        """Ejecuta las consultas guardadas en sql/consultas.sql."""
        consultas = self._load_statements(CONSULTAS_PATH)
        resultados: List[QueryResult] = []
        with self.connect() as conexion:
            cursor = conexion.cursor()
            for sentencia in consultas:
                cursor.execute(sentencia)
                filas = [tuple(fila) for fila in cursor.fetchall()]
                headers = [col[0] for col in cursor.description] if cursor.description else []
                resultados.append(QueryResult(sentencia, headers, filas))
        return resultados

    def export_reports(self, resultados: Sequence[QueryResult]) -> None:
        """Exporta cada consulta a un archivo CSV dentro de data/reportes."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        for indice, resultado in enumerate(resultados, start=1):
            nombre = REPORTS_DIR / f"reporte_{indice:02d}.csv"
            with nombre.open("w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                if resultado.headers:
                    writer.writerow(resultado.headers)
                writer.writerows(resultado.rows)
            print(f"-> Reporte generado: {nombre}")

    def run_checks(self) -> None:
        """Comprueba que se cumplan los requisitos típicos del proyecto final."""
        print("\nValidando requisitos del proyecto final...")
        checks = [
            ("Tablas principales creadas", self._check_tables),
            ("Vista de resumen disponible", self._check_view),
            ("Triggers de control de porcentajes activos", self._check_triggers),
            ("Porcentajes de evaluaciones suman 100", self._check_percentages),
            ("Datos de ejemplo cargados", self._check_sample_data),
        ]
        for nombre, funcion in checks:
            try:
                exito, detalle = funcion()
            except sqlite3.DatabaseError as error:
                exito = False
                detalle = str(error)
            estado = "OK" if exito else "FALTA"
            print(f"[{estado}] {nombre}")
            if detalle:
                print(f"      {detalle}")

    def launch_menu(self) -> None:
        """Menú interactivo para gestionar la base de datos a mano."""
        print("\n=== Menú interactivo del proyecto académico ===")
        acciones = {
            "1": ("Listar estudiantes con sus cursos", self._menu_list_students),
            "2": ("Registrar nuevo estudiante", self._menu_add_student),
            "3": ("Matricular estudiante en un curso", self._menu_enroll_student),
            "4": ("Registrar calificación de una evaluación", self._menu_register_grade),
            "5": ("Generar reportes en CSV", self._menu_generate_reports),
            "0": ("Salir", None),
        }
        while True:
            for clave, (descripcion, _) in acciones.items():
                print(f"  {clave}. {descripcion}")
            opcion = input("Selecciona una opción: ").strip()
            if opcion == "0":
                print("Saliendo del menú...")
                break
            accion = acciones.get(opcion)
            if not accion:
                print("Opción no válida. Intenta de nuevo.\n")
                continue
            _, funcion = accion
            if funcion:
                try:
                    funcion()
                except sqlite3.IntegrityError as error:
                    print(f"Ocurrió un problema de integridad: {error}\n")
                except sqlite3.DatabaseError as error:
                    print(f"Error de base de datos: {error}\n")

    # ----- Métodos privados de apoyo -----

    def _run_script(self, conexion: sqlite3.Connection, ruta_sql: Path) -> None:
        with ruta_sql.open("r", encoding="utf-8") as archivo_sql:
            conexion.executescript(archivo_sql.read())

    def _load_statements(self, ruta_sql: Path) -> List[str]:
        consultas: List[str] = []
        sentencia_actual: List[str] = []
        with ruta_sql.open("r", encoding="utf-8") as archivo:
            for linea in archivo:
                limpia = linea.strip()
                if not limpia or limpia.startswith("--"):
                    continue
                sentencia_actual.append(limpia)
                if limpia.endswith(";"):
                    sentencia = " ".join(sentencia_actual)[:-1].strip()
                    consultas.append(sentencia)
                    sentencia_actual = []
        return consultas

    def _check_tables(self) -> tuple[bool, str]:
        esperadas = {"estudiantes", "profesores", "cursos", "matriculas", "evaluaciones", "calificaciones"}
        with self.connect() as conexion:
            cursor = conexion.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existentes = {fila[0] for fila in cursor}
        faltantes = esperadas - existentes
        return (not faltantes, "" if not faltantes else f"Faltan: {', '.join(sorted(faltantes))}")

    def _check_view(self) -> tuple[bool, str]:
        with self.connect() as conexion:
            cursor = conexion.execute(
                "SELECT name FROM sqlite_master WHERE type='view' AND name='vw_resumen_estudiantes';"
            )
            existe = cursor.fetchone() is not None
        return existe, "" if existe else "Crea la vista vw_resumen_estudiantes ejecutando schema.sql"

    def _check_triggers(self) -> tuple[bool, str]:
        necesarios = {"trg_validar_porcentaje_insert", "trg_validar_porcentaje_update"}
        with self.connect() as conexion:
            cursor = conexion.execute("SELECT name FROM sqlite_master WHERE type='trigger';")
            existentes = {fila[0] for fila in cursor}
        faltantes = necesarios - existentes
        return (not faltantes, "" if not faltantes else f"Faltan: {', '.join(sorted(faltantes))}")

    def _check_percentages(self) -> tuple[bool, str]:
        with self.connect() as conexion:
            cursor = conexion.execute(
                """
                SELECT c.nombre, COALESCE(SUM(ev.porcentaje), 0) AS total
                FROM cursos c
                LEFT JOIN evaluaciones ev ON ev.curso_id = c.id
                GROUP BY c.id
                HAVING total != 100
                """
            )
            inconsistencias = cursor.fetchall()
        if inconsistencias:
            detalle = "; ".join(f"{fila['nombre']} tiene {fila['total']}%" for fila in inconsistencias)
            return False, detalle
        return True, ""

    def _check_sample_data(self) -> tuple[bool, str]:
        with self.connect() as conexion:
            estudiantes = conexion.execute("SELECT COUNT(*) FROM estudiantes;").fetchone()[0]
            cursos = conexion.execute("SELECT COUNT(*) FROM cursos;").fetchone()[0]
            matriculas = conexion.execute("SELECT COUNT(*) FROM matriculas;").fetchone()[0]
        ok = estudiantes >= 4 and cursos >= 3 and matriculas >= 5
        detalle = f"Estudiantes: {estudiantes}, cursos: {cursos}, matrículas: {matriculas}"
        return ok, detalle

    def _menu_list_students(self) -> None:
        consulta = (
            """
            SELECT e.id, e.nombre, e.email,
                   GROUP_CONCAT(DISTINCT c.nombre, ', ') AS cursos,
                   ROUND(AVG(cal.nota), 2) AS nota_media
            FROM estudiantes e
            LEFT JOIN matriculas m ON m.estudiante_id = e.id
            LEFT JOIN cursos c ON c.id = m.curso_id
            LEFT JOIN calificaciones cal ON cal.matricula_id = m.id
            GROUP BY e.id
            ORDER BY e.nombre;
            """
        )
        self._print_query(consulta)

    def _menu_add_student(self) -> None:
        print("\nIntroduce los datos del nuevo estudiante")
        nombre = input("Nombre completo: ").strip()
        email = input("Correo electrónico: ").strip()
        telefono = input("Teléfono (opcional): ").strip()
        if not nombre or not email:
            print("Nombre y correo son obligatorios. Operación cancelada.\n")
            return
        with self.connect() as conexion:
            conexion.execute(
                "INSERT INTO estudiantes (nombre, email, telefono) VALUES (?, ?, ?);",
                (nombre, email, telefono or None),
            )
            conexion.commit()
        print("Estudiante registrado correctamente.\n")

    def _menu_enroll_student(self) -> None:
        print("\nEstudiantes disponibles:")
        self._print_query("SELECT id, nombre FROM estudiantes ORDER BY id;")
        print("\nCursos disponibles:")
        self._print_query("SELECT id, nombre, cupo_maximo FROM cursos ORDER BY id;")
        try:
            estudiante_id = int(input("ID del estudiante: ").strip())
            curso_id = int(input("ID del curso: ").strip())
        except ValueError:
            print("IDs no válidos. Operación cancelada.\n")
            return
        estado = input("Estado inicial (activa/aprobada/reprobada/retirada) [activa]: ").strip() or "activa"
        if estado not in {"activa", "aprobada", "reprobada", "retirada"}:
            print("Estado no válido. Operación cancelada.\n")
            return
        with self.connect() as conexion:
            conexion.execute(
                "INSERT INTO matriculas (estudiante_id, curso_id, estado) VALUES (?, ?, ?);",
                (estudiante_id, curso_id, estado),
            )
            conexion.commit()
        print("Matrícula registrada correctamente.\n")

    def _menu_register_grade(self) -> None:
        print("\nMatrículas activas:")
        self._print_query(
            """
            SELECT m.id, e.nombre AS estudiante, c.nombre AS curso, m.estado
            FROM matriculas m
            JOIN estudiantes e ON e.id = m.estudiante_id
            JOIN cursos c ON c.id = m.curso_id
            WHERE m.estado != 'retirada'
            ORDER BY m.id;
            """
        )
        print("\nEvaluaciones disponibles:")
        self._print_query(
            """
            SELECT ev.id, c.nombre AS curso, ev.nombre AS evaluacion, ev.porcentaje
            FROM evaluaciones ev
            JOIN cursos c ON c.id = ev.curso_id
            ORDER BY ev.id;
            """
        )
        try:
            matricula_id = int(input("ID de la matrícula: ").strip())
            evaluacion_id = int(input("ID de la evaluación: ").strip())
            nota = float(input("Nota (0-10): ").strip())
        except ValueError:
            print("Datos no válidos. Operación cancelada.\n")
            return
        if not 0 <= nota <= 10:
            print("La nota debe estar entre 0 y 10.\n")
            return
        with self.connect() as conexion:
            conexion.execute(
                "INSERT OR REPLACE INTO calificaciones (matricula_id, evaluacion_id, nota) VALUES (?, ?, ?);",
                (matricula_id, evaluacion_id, nota),
            )
            conexion.commit()
            self._actualizar_estado_matricula(conexion, matricula_id)
        print("Calificación registrada correctamente.\n")

    def _menu_generate_reports(self) -> None:
        resultados = self.run_saved_queries()
        self.export_reports(resultados)
        print("Reportes creados en la carpeta data/reportes.\n")

    def _print_query(self, sql: str) -> None:
        with self.connect() as conexion:
            cursor = conexion.execute(sql)
            filas = [tuple(fila) for fila in cursor.fetchall()]
            headers = [col[0] for col in cursor.description] if cursor.description else []
        if not filas:
            print("  (sin datos)")
            return
        widths = [max(len(str(fila[idx])) for fila in filas + [headers]) for idx in range(len(headers))]
        cabecera = " | ".join(str(header).ljust(widths[idx]) for idx, header in enumerate(headers))
        print(cabecera)
        print("-" * len(cabecera))
        for fila in filas:
            print(" | ".join(str(fila[idx]).ljust(widths[idx]) for idx in range(len(headers))))
        print("")

    def _actualizar_estado_matricula(self, conexion: sqlite3.Connection, matricula_id: int) -> None:
        estado_actual = conexion.execute(
            "SELECT estado FROM matriculas WHERE id = ?;", (matricula_id,)
        ).fetchone()
        if estado_actual is None or estado_actual[0] == "retirada":
            return
        datos = conexion.execute(
            """
            SELECT
                SUM(ev.porcentaje) AS total_porcentaje,
                SUM(CASE WHEN cal.nota IS NOT NULL THEN ev.porcentaje ELSE 0 END) AS porcentaje_calificado,
                AVG(cal.nota) AS nota_media
            FROM matriculas m
            JOIN cursos c ON c.id = m.curso_id
            JOIN evaluaciones ev ON ev.curso_id = c.id
            LEFT JOIN calificaciones cal ON cal.evaluacion_id = ev.id AND cal.matricula_id = m.id
            WHERE m.id = ?;
            """,
            (matricula_id,),
        ).fetchone()
        if datos is None or datos[0] is None:
            return
        total_porcentaje, porcentaje_calificado, nota_media = datos
        if total_porcentaje == porcentaje_calificado and nota_media is not None:
            nuevo_estado = "aprobada" if nota_media >= 5 else "reprobada"
            conexion.execute(
                "UPDATE matriculas SET estado = ? WHERE id = ?;", (nuevo_estado, matricula_id)
            )
            conexion.commit()
        elif porcentaje_calificado > 0:
            conexion.execute("UPDATE matriculas SET estado = 'activa' WHERE id = ?;", (matricula_id,))
            conexion.commit()


def display_results(resultados: Sequence[QueryResult]) -> None:
    """Muestra en pantalla los resultados de las consultas guardadas."""
    for indice, resultado in enumerate(resultados, start=1):
        print(f"\nResultado de la consulta {indice}:")
        print(f"SQL: {resultado.sql}")
        if not resultado.rows:
            print("  (sin datos)")
            continue
        widths = [
            max(len(str(fila[idx])) for fila in list(resultado.rows) + [resultado.headers])
            for idx in range(len(resultado.headers))
        ]
        cabecera = " | ".join(str(header).ljust(widths[idx]) for idx, header in enumerate(resultado.headers))
        print(cabecera)
        print("-" * len(cabecera))
        for fila in resultado.rows:
            print(" | ".join(str(fila[idx]).ljust(widths[idx]) for idx in range(len(resultado.headers))))
    print("")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Herramienta de apoyo para el proyecto final de Ampliación de Bases de Datos",
    )
    parser.add_argument(
        "--init-only",
        action="store_true",
        help="Reinicia la base de datos y termina sin ejecutar más acciones",
    )
    parser.add_argument(
        "--sin-datos",
        action="store_true",
        help="Al reiniciar, no carga los datos de ejemplo (BD vacía)",
    )
    parser.add_argument(
        "--reiniciar",
        action="store_true",
        help="Recrea la base de datos antes de ejecutar las acciones solicitadas",
    )
    parser.add_argument(
        "--consultas",
        action="store_true",
        help="Muestra en pantalla las consultas guardadas",
    )
    parser.add_argument(
        "--exportar-reportes",
        action="store_true",
        help="Genera los CSV dentro de data/reportes",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Ejecuta las comprobaciones del proyecto final",
    )
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Abre el menú interactivo para gestionar la base de datos",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manager = DatabaseManager()

    if args.init_only:
        manager.initialize(with_sample_data=not args.sin_datos)
        return

    if args.menu:
        if args.reiniciar:
            manager.initialize(with_sample_data=not args.sin_datos)
        else:
            manager.ensure_database()
        manager.launch_menu()
        return

    acciones_directas = args.consultas or args.exportar_reportes or args.check
    if acciones_directas:
        if args.reiniciar:
            manager.initialize(with_sample_data=not args.sin_datos)
        else:
            manager.ensure_database()
    resultados_cache: List[QueryResult] | None = None

    if args.consultas:
        resultados_cache = manager.run_saved_queries()
        display_results(resultados_cache)

    if args.exportar_reportes:
        if resultados_cache is None:
            resultados_cache = manager.run_saved_queries()
        manager.export_reports(resultados_cache)

    if args.check:
        manager.run_checks()

    if not acciones_directas:
        # Ejecución por defecto (pipeline completo para la entrega final)
        manager.initialize(with_sample_data=not args.sin_datos)
        resultados_cache = manager.run_saved_queries()
        display_results(resultados_cache)
        manager.export_reports(resultados_cache)
        manager.run_checks()


if __name__ == "__main__":
    main()
