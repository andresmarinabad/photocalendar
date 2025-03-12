import sqlite3
from config import config


def create_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia INTEGER,
                titulo TEXT,
                opciones TEXT,
                mes TEXT
            )
        """)
    conn.commit()
    conn.close()


def get_connection():
    """Establece la conexión a la base de datos SQLite."""
    return sqlite3.connect(config.DB_PATH)


def get_tables(pd):
    """Obtiene una lista de tablas en la base de datos."""
    conn = get_connection()
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'",
        conn
    )["name"].tolist()
    conn.close()
    return tables


def get_all_from_table(table, pd):
    conn = get_connection()
    info = pd.read_sql(
        f"SELECT dia, titulo, opciones, mes FROM {table} ORDER BY mes",
        conn
    )
    conn.close()
    return info


def load_data(table_name, pd):
    """Carga los datos de una tabla específica."""
    conn = get_connection()
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        if df.empty:
            return pd.DataFrame()  # Si no hay datos, retorna un DataFrame vacío
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()  # Si ocurre un error, retorna un DataFrame vacío
    finally:
        conn.close()
    return df


def insert_data(table_name, dia, titulo, opciones, mes):
    """Inserta un nuevo registro en la tabla seleccionada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {table_name} (dia, titulo, opciones, mes) VALUES (?, ?, ?, ?)
    """, (dia, titulo, opciones, mes))
    conn.commit()
    conn.close()


def update_record(table_name, record_id, new_data):
    """Actualiza un registro en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Construir el SET para la consulta SQL dinámicamente
    set_clause = ", ".join([f"{col} = ?" for col in new_data.keys()])
    values = list(new_data.values()) + [record_id]

    sql = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
    cursor.execute(sql, values)
    
    conn.commit()
    conn.close()


def delete_records(table_name, ids_to_delete):
    """Elimina registros seleccionados de la base de datos."""
    if not ids_to_delete:
        return  # No hacer nada si no hay selección

    conn = get_connection()
    cursor = conn.cursor()
    
    # Construir consulta con placeholders dinámicos
    sql = f"DELETE FROM {table_name} WHERE id IN ({','.join(['?']*len(ids_to_delete))})"
    cursor.execute(sql, ids_to_delete)

    conn.commit()
    conn.close()


def table_is_empty(table_name):
    """Verifica si una tabla está vacía."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0
