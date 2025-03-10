# PhotoCalendar

PhotoCalendar es una aplicación en Python que permite gestionar un calendario fotográfico personalizado. Carga información desde un archivo CSV, la almacena en una base de datos SQLite local y muestra los datos con Streamlit. Desde la interfaz web, los usuarios pueden añadir, modificar y eliminar eventos. Además, se puede exportar la información a un archivo LaTeX (`.tex`) y compilarlo en un PDF con diseño personalizado.

---

## Características principales

- **Carga de eventos desde un archivo CSV**
- **Almacenamiento en SQLite** para persistencia de datos
- **Interfaz web con Streamlit** para visualizar y gestionar eventos
- **Exportación a LaTeX (`.tex`)** para generar una plantilla de calendario
- **Compilación a PDF** desde la interfaz web
- **Soporte para imágenes** personalizadas por mes (`mes.jpeg` en castellano)
- **Inclusión de días festivos fijos y móviles** (Navidad, Año Nuevo, etc.)

---

## Requisitos de instalación

### 1. Instalar Python
PhotoCalendar requiere **Python 3.8 o superior**. Puedes comprobar tu versión con:
```bash
python --version
```
Si no lo tienes instalado, descárgalo desde [python.org](https://www.python.org/downloads/).

### 2. Crear un entorno virtual (opcional, pero recomendado)
```bash
python -m venv env
source env/bin/activate  # En Linux/macOS
env\Scripts\activate    # En Windows
```

### 3. Instalar dependencias
Ejecuta el siguiente comando en la terminal:
```bash
pip install -r requirements.txt
```
El archivo `requirements.txt` debe contener:
```
streamlit
pandas
sqlite3
latex
```

### 4. Instalar LaTeX para la generación de PDF
Necesitas un compilador de LaTeX como **TeX Live** o **MiKTeX**:
- **Ubuntu/Debian:**
  ```bash
  sudo apt install texlive-full
  ```
- **Windows:** Descarga [MiKTeX](https://miktex.org/download).
- **Mac:**
  ```bash
  brew install mactex
  ```

---

## Uso de la aplicación

### 1. Preparar los archivos
- Asegúrate de tener un archivo CSV con los eventos.
- Las imágenes deben estar en la carpeta de imágenes y nombradas según el mes: `enero.jpeg`, `febrero.jpeg`, etc.

### 2. Ejecutar la aplicación
Inicia la interfaz de Streamlit con:
```bash
streamlit run app.py
```
Esto abrirá la aplicación en tu navegador.

### 3. Gestionar eventos
Desde la interfaz puedes:
- **Cargar eventos** desde el CSV
- **Agregar, modificar y eliminar eventos** en la base de datos SQLite

### 4. Exportar el calendario a LaTeX y PDF
- Presiona el botón **"Exportar a LaTeX"** para generar el archivo `.tex`
- Presiona **"Compilar PDF"** para generar el calendario en formato PDF

---

## Estructura del Proyecto
```bash
├── build
│   ├── calendar.sty
│   └── calendar.tex
├── data
│   ├── data.csv
│   └── data.db
├── LICENSE
├── README.md
├── src
│   ├── config.py
│   ├── database.py
│   ├── data.py
│   ├── __init__.py
│   ├── app.py
│   ├── render.py
│   ├── template
│   │   └── plantilla_imagen.xcf
│   └── utils.py
└── templates
    └── header
```

---

## Contribuir
Si quieres mejorar este proyecto, sigue estos pasos:
1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/PhotoCalendar.git
   ```
2. **Crea una rama:**
   ```bash
   git checkout -b mi-mejora
   ```
3. **Haz tus cambios y súbelos:**
   ```bash
   git add .
   git commit -m "Mejoras en la exportación a LaTeX"
   git push origin mi-mejora
   ```
4. **Haz un Pull Request en GitHub.**

---

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente.

---

✨ **Disfruta creando tu calendario fotográfico personalizado!** 📅🎨

