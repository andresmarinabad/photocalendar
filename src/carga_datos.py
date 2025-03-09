import sqlite3
import pandas as pd
import glob
import os

# Conexión a SQLite
db_path = "../data/datos.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS marin_codina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia INTEGER,
        titulo TEXT,
        opciones TEXT,
        mes TEXT
    )
""")
conn.commit()

# Obtener los archivos CSV de los meses
archivos = glob.glob("../data/*.csv")

# Nombres de meses esperados
meses_validos = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

for archivo in archivos:
    nombre_mes = os.path.splitext(archivo)[0].lower().split('/')[-1]
    
    if nombre_mes in meses_validos:
        print(f"Procesando {archivo}...")
        df = pd.read_csv(archivo)

        # Agregar columna del mes
        df["mes"] = nombre_mes

        # Verificar si los datos ya existen en la tabla
        query = f"SELECT COUNT(*) FROM marin_codina WHERE mes = ?"
        cursor.execute(query, (nombre_mes,))
        count = cursor.fetchone()[0]

        if count == 0:
            df.to_sql("marin_codina", conn, if_exists="append", index=False)
            print(f"Datos de {archivo} cargados en la base de datos.")
        else:
            print(f"Los datos de {archivo} ya existen. No se cargan nuevamente.")

# Cerrar la conexión
conn.close()
print("Proceso finalizado.")