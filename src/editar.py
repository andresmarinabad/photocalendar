import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "../data/datos.db"

def get_connection():
    """Establece la conexión a la base de datos."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def load_data(table_name):
    """Carga los datos de la tabla seleccionada."""
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def update_record(table_name, record_id, dia, titulo, opciones, mes):
    """Actualiza un registro en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {table_name} 
        SET dia = ?, titulo = ?, opciones = ?, mes = ? 
        WHERE id = ?
    """, (dia, titulo, opciones, mes, record_id))
    conn.commit()
    conn.close()

# === UI PRINCIPAL ===
st.title("✏️ Modificar Registros en SQLite")

# === SELECCIONAR TABLA ===
conn = get_connection()
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)["name"].tolist()
conn.close()

if not tables:
    st.error("⚠️ No hay tablas en la base de datos.")
    st.stop()

tabla_seleccionada = st.selectbox("📂 Selecciona una tabla:", tables)

# === CARGAR Y MOSTRAR DATOS ===
df = load_data(tabla_seleccionada)

if df.empty:
    st.warning("⚠️ No hay datos en esta tabla.")
    st.stop()

# Seleccionar registro a modificar
st.subheader("📋 Registros Actuales")
record_id = st.selectbox("Selecciona un registro para editar:", df["id"].tolist())

# Obtener datos del registro seleccionado
registro_actual = df[df["id"] == record_id].iloc[0]

# === FORMULARIO PARA EDITAR ===
st.sidebar.header("✏️ Editar Registro")

with st.sidebar.form(key="form_editar"):
    dia = st.number_input("Día", min_value=1, max_value=31, step=1, value=int(registro_actual["dia"]))
    titulo = st.text_input("Título", value=registro_actual["titulo"])
    opciones = st.text_area("Opciones", value=registro_actual["opciones"])
    mes = st.selectbox("Mes", [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ], index=["enero", "febrero", "marzo", "abril", "mayo", "junio",
              "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"].index(registro_actual["mes"]))

    submit_button = st.form_submit_button("Actualizar Registro")

if submit_button:
    update_record(tabla_seleccionada, record_id, dia, titulo, opciones, mes)
    st.sidebar.success("✅ Registro actualizado correctamente.")
    st.experimental_rerun()  # Recargar la app para actualizar los datos
