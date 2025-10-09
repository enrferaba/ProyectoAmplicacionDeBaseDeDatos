"""Proyecto de ejemplo para la asignatura de Ampliación de Bases de Datos.
Este script genera una base de datos SQLite muy sencilla con datos de prueba
para poder practicar consultas y procesos ETL básicos.
"""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "academico.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
DATA_PATH = BASE_DIR / "sql" / "data.sql"
CONSULTAS_PATH = BASE_DIR / "sql" / "consultas.sql"


def cargar_sql(descriptor: sqlite3.Cursor, ruta_sql: Path) -> None:
    """Lee un archivo .sql y ejecuta cada sentencia contra la base de datos."""
    with ruta_sql.open("r", encoding="utf-8") as archivo_sql:
        sentencias = archivo_sql.read()
        descriptor.executescript(sentencias)


def inicializar_bd() -> None:
    """Crea la base de datos desde cero y carga los datos de ejemplo."""
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as conexion:
        cursor = conexion.cursor()
        cargar_sql(cursor, SCHEMA_PATH)
        cargar_sql(cursor, DATA_PATH)
        conexion.commit()


def ejecutar_consultas() -> list[list[str]]:
    """Ejecuta las consultas de ejemplo y devuelve los resultados en memoria."""
    resultados = []
    with sqlite3.connect(DATABASE_PATH) as conexion:
        cursor = conexion.cursor()
        with CONSULTAS_PATH.open("r", encoding="utf-8") as archivo:
            consulta_actual = ""
            for linea in archivo:
                linea_limpia = linea.strip()
                if not linea_limpia or linea_limpia.startswith("--"):
                    continue
                consulta_actual += " " + linea_limpia
                if linea_limpia.endswith(";"):
                    cursor.execute(consulta_actual)
                    resultados.append(cursor.fetchall())
                    consulta_actual = ""
    return resultados


def mostrar_resultados(resultados: list[list[tuple]]) -> None:
    """Imprime de forma amigable los resultados de las consultas."""
    for numero, filas in enumerate(resultados, start=1):
        print(f"\nResultado de la consulta {numero}:")
        if not filas:
            print("  (sin datos)")
            continue
        for fila in filas:
            print("  - ", fila)


if __name__ == "__main__":
    print("Iniciando creación de la base de datos...")
    inicializar_bd()
    print(f"Base de datos creada en: {DATABASE_PATH}")
    print("Ejecutando consultas de ejemplo...")
    resultados_consultas = ejecutar_consultas()
    mostrar_resultados(resultados_consultas)
    print("\nProceso finalizado. Puedes revisar el archivo academico.db para más pruebas.")
