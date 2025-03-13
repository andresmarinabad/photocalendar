import os
import glob
from config import config
from database import (get_connection,
                      create_table,
                      table_is_empty, 
                      get_tables,
                      get_all_from_table)
from utils import consultar_leyenda, calcular_eventos_calendario


def load_csv_data(pd, st):
    """Carga automáticamente los CSV si las tablas están vacías."""

    # Buscar archivos CSV en la carpeta
    csv_files = glob.glob(os.path.join(config.CSV_FOLDER, "*.csv"))

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

        create_table(config.TABLE_NAME)

        # Insertar solo si la tabla está vacía
        if table_is_empty(config.TABLE_NAME):
            conn = get_connection()
            df.to_sql(config.TABLE_NAME, conn, if_exists="append", index=False)
            st.success(f"✅ Datos de {mes} cargados en la base de datos.")

    st.rerun()


def load_all_days(df):
    todos_dias = {}
    eventos = calcular_eventos_calendario()
    for mes, grupo in df.groupby('mes'):
        for dia in range(1, 32):
            fiesta = ''
            if mes in eventos and dia in eventos[mes]:
                fiesta = eventos[mes][dia]
            resultado = grupo[grupo['dia'] == dia]
            clave = f'{mes}{dia}'
            este_dia = ''
            if not resultado.empty:
                info_list = resultado[['titulo', 'opciones']].values.flatten().tolist()
                for titulo, opciones in zip(info_list[::2], info_list[1::2]):
                    text = consultar_leyenda(titulo, opciones)
                    if este_dia != '':
                        este_dia = f'{este_dia}\\\\{text}'
                    else:
                        este_dia = f'{text}'
                 
            todos_dias[clave] = "\\day{"+fiesta+"}{\\vspace{1.75cm}"+este_dia+"}\n"

    return todos_dias


def export_data_csv(pd):
    try:

        tables = get_tables(pd)
        output_path = os.path.join(config.ROOT, 'data')
        output_folder = output_path

        for table_name in tables:
            output_file = f"{output_folder}/{table_name}.csv"
            
            info = get_all_from_table(table_name, pd)
            
            # Exportar a CSV
            info.to_csv(output_file, index=False)
        
        print("Exportación completada con éxito.")
        return True
    except Exception as e:
        print(f"Error al exportar datos: {e}")
        return False
