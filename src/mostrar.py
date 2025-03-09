import streamlit as st
import sqlite3
import pandas as pd
import glob
import os


DB_PATH = "../data/data.db"
CSV_FOLDER = "../data"
TABLE_NAME = "marin_codina"


def get_connection():
    """Establece la conexión a la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)


def get_tables():
    """Obtiene una lista de tablas en la base de datos."""
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
        mes = os.path.basename(file).replace(".csv", "")  
        df = pd.read_csv(file)

        # Verificar que el CSV tiene las columnas esperadas
        if not {"dia", "titulo", "opciones", "mes"}.issubset(df.columns):
            st.error(f"⚠️ El archivo {file} no tiene las columnas correctas.")
            continue

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia INTEGER,
                titulo TEXT,
                opciones TEXT,
                mes TEXT
            )
        """)

        # Insertar solo si la tabla está vacía
        if table_is_empty(TABLE_NAME):
            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
            st.success(f"✅ Datos de {mes} cargados en la base de datos.")

    conn.commit()
    conn.close()
    st.rerun()


# === UI PRINCIPAL CON STREAMLIT ===
st.set_page_config(page_title="PhotoCalendar", 
                   page_icon="📊",
                   layout="wide"
)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton  {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title("PhotoCalendar -- datos")

# === SELECCIONAR TABLA PARA VISUALIZAR ===
tablas = get_tables()
if not tablas:
    if st.button("📂 Cargar CSV de inicio"):
        load_csv_data()
        #st.rerun()

tabla_seleccionada = st.selectbox("📂 Selecciona una tabla:", tablas)

# === CARGAR Y MOSTRAR DATOS DE LA TABLA ===
try:
    df = load_data(tabla_seleccionada)
    if df.empty:
        st.warning("⚠️ No hay datos cargados.")
        st.stop()
except Exception as e:
    df = pd.DataFrame() 
    st.warning("⚠️ Hubo un error al cargar los datos.")

if not df.empty:
    # Filtro por mes
    meses = df["mes"].unique().tolist()
    mes_seleccionado = st.selectbox("📅 Filtra por mes:", ["Todos"] + meses)

    if mes_seleccionado != "Todos":
        df = df[df["mes"] == mes_seleccionado]

    # Mostrar la tabla
    #st.dataframe(df, hide_index=True)
    # ✅ Asegurar que 'id' no sea editable
    df.set_index("id", inplace=True)  # Usamos ID como índice para evitar su modificación

    # ✅ Hacer que solo las otras columnas sean editables
    editable_columns = [col for col in df.columns if col != "id"]
    df["Eliminar"] = False
    edited_df = st.data_editor(df, use_container_width=True, hide_index=True)

    # === ELIMINAR REGISTROS ===
    ids_to_delete = edited_df[edited_df["Eliminar"]].index.tolist()

    if ids_to_delete and st.button("🗑️ Eliminar seleccionados"):
        delete_records(tabla_seleccionada, ids_to_delete)
        st.success(f"✅ {len(ids_to_delete)} registros eliminados correctamente.")
        st.rerun()  # Recargar la tabla

    # === DETECTAR CAMBIOS Y ACTUALIZAR ===
    df.drop(columns=["Eliminar"], inplace=True, errors="ignore")
    edited_df.drop(columns=["Eliminar"], inplace=True, errors="ignore")

    # === DETECTAR CAMBIOS Y ACTUALIZAR ===
    if not edited_df.equals(df): 
        for record_id in edited_df.index:
            new_data = edited_df.loc[record_id].to_dict()
            update_record(tabla_seleccionada, record_id, new_data)
            
        st.success("✅ Datos actualizados correctamente.")
        st.rerun()


# === FORMULARIO PARA AGREGAR NUEVOS REGISTROS ===
st.sidebar.header("➕ Agregar datos")

with st.sidebar.form(key="form_registro"):
    dia = st.number_input("Día", min_value=1, max_value=31, step=1)
    titulo = st.text_input("Título")
    opciones = st.text_area("Opciones")
    mes = st.selectbox("Mes", [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ])
    
    submit_button = st.form_submit_button("Guardar")

if submit_button:
    if titulo and opciones:
        insert_data(tabla_seleccionada, dia, titulo, opciones, mes)
        st.sidebar.success(f"✅ Registro guardado en {tabla_seleccionada}.")
        st.rerun()  # Recargar la app para actualizar los datos
    else:
        st.sidebar.error("⚠️ Título y Opciones son obligatorios.")

st.sidebar.info("📌 Usa el formulario para agregar datos a la tabla seleccionada.")