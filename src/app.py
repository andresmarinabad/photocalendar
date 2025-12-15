import os
import streamlit as st
import pandas as pd
from datos import load_csv_data, load_all_days, export_data_csv
from utils import create_calendar_tex, compile_pdf
from database import (get_tables,
                      load_data,
                      delete_records,
                      update_record,
                      insert_data)


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
tablas = get_tables(pd)
if not tablas:
    if st.button("📂 Cargar CSV de inicio"):
        load_csv_data(pd, st)
        st.rerun()


tabla_seleccionada = st.selectbox("📂 Selecciona una tabla:", tablas)

# === CARGAR Y MOSTRAR DATOS DE LA TABLA ===
try:
    df = load_data(tabla_seleccionada, pd)
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

    export = st.button("Exportar datos a csv", type="secondary")

    if export:
        exportado = export_data_csv(pd)

        if exportado:
            st.toast("Datos exportados a csv")

gen_pdf = st.button("Crear Calendario", type="primary")
if gen_pdf:
    with st.spinner("Exportando a pdf..."):
        if df.empty:
            meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                             'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
            df = pd.DataFrame(meses, columns=['mes'])
        days = load_all_days(df)
        create_calendar_tex(days)
        compilado = compile_pdf()
        

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