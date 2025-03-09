import streamlit as st
import sqlite3
import pandas as pd
import os
import glob

DB_PATH = "datos.db"
CSV_FOLDER = "./csv_data"  # Carpeta donde están los CSV

def get_connection():
    """Establece la conexión con SQLite."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def get_tables():
    """Obtiene las tablas en la base de datos, excluyendo sqlite_sequence."""
    conn = get_connection()
    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'",
        conn
    )["name"].tolist()
    conn.close()
    return tables

def load_data(table_name):
    """Carga los datos de una tabla específica."""
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def table_is_empty(table_name):
    """Verifica si una tabla está vacía."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def load_csv_data():
    """Carga automáticamente los CSV si las tablas están vacías."""
    conn = get_connection()
    cursor = conn.cursor()

    # Buscar archivos CSV en la carpeta
    csv_files = glob.glob(os.path.join(CSV_FOLDER, "*.csv"))

    if not csv_files:
        st.error("⚠️ No se encontraron archivos CSV en la carpeta.")
        return

    for file in csv_files:
        mes = os.path.basename(file).replace(".csv", "")  # Extraer el mes del nombre del archivo
        df = pd.read_csv(file)

        # Verificar que el CSV tiene las columnas esperadas
        if not {"día", "título", "opciones"}.issubset(df.columns):
            st.error(f"⚠️ El archivo {file} no tiene las columnas correctas.")
            continue

        table_name = mes.lower()  # Nombre de tabla basado en el mes
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia INTEGER,
                titulo TEXT,
                opciones TEXT,
                mes TEXT
            )
        """)

        # Insertar solo si la tabla está vacía
        if table_is_empty(table_name):
            df["mes"] = mes  # Agregar el mes como columna
            df.to_sql(table_name, conn, if_exists="append", index=False)
            st.success(f"✅ Datos de {mes} cargados en la base de datos.")

    conn.commit()
    conn.close()

# === UI PRINCIPAL ===
st.title("📊 Gestión de Registros en SQLite")

# === BOTÓN PARA CARGAR CSV SI NO HAY DATOS ===
tables = get_tables()

if not tables:
    st.warning("⚠️ No hay tablas en la base de datos. Carga los datos iniciales.")
    if st.button("📂 Cargar CSV de inicio"):
        load_csv_data()
        st.experimental_rerun()

# === SELECCIONAR TABLA SI EXISTE ===
if tables:
    tabla_seleccionada = st.selectbox("📂 Selecciona una tabla:", tables)

    # Cargar y mostrar datos
    df = load_data(tabla_seleccionada)

    if df.empty:
        st.warning(f"⚠️ La tabla {tabla_seleccionada} está vacía.")
    else:
        st.dataframe(df, use_container_width=True)
