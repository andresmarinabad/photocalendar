# PhotoCalendar

PhotoCalendar es una aplicación en Python que permite gestionar un calendario fotográfico personalizado. Carga información desde archivos CSV, los cuales generan las tablas internas en una base de datos SQLite local y muestran los datos con Streamlit. El nombre de cada archivo CSV importado se usa como nombre de la tabla correspondiente. Si no hay datos en los archivos CSV, también es posible generar un calendario vacío.

Desde la interfaz web, los usuarios pueden añadir, modificar y eliminar eventos. Además, se puede exportar la información a un archivo LaTeX (`.tex`) y compilarlo en un PDF con diseño personalizado.

---

![Static Badge](https://img.shields.io/badge/python-v3.12-green)
![Static Badge](https://img.shields.io/badge/python-streamlit-orange)
![Static Badge](https://img.shields.io/badge/tex-latex-blue)
![Static Badge](https://img.shields.io/badge/bash-sh-yellow)

## Características principales

- **Carga de eventos desde archivos CSV** (el nombre del archivo define el nombre de la tabla en SQLite)
- **Almacenamiento en SQLite** para persistencia de datos
- **Interfaz web con Streamlit** para visualizar y gestionar eventos
- **Exportación a LaTeX (`.tex`)** para generar una plantilla de calendario
- **Compilación a PDF** desde la interfaz web
- **Soporte para imágenes** personalizadas por mes (`mes.jpeg` en castellano)
- **Inclusión de días festivos fijos y móviles** (Navidad, Año Nuevo, etc.)

---

## Requisitos de instalación

### 1. Instalación manual

#### Instalar Python
PhotoCalendar requiere **Python 3.8 o superior**. Puedes comprobar tu versión con:
```bash
python --version
```
Si no lo tienes instalado, descárgalo desde [python.org](https://www.python.org/downloads/).

#### Crear un entorno virtual (opcional, pero recomendado)
```bash
python -m venv env
source env/bin/activate  # En Linux/macOS
env\Scripts\activate    # En Windows
```

#### Instalar dependencias
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

#### Instalar LaTeX para la generación de PDF
Necesitas un compilador de LaTeX como **TeX Live** o **MiKTeX**:

  ```bash
  sudo apt install texlive texlive-latex-extra texlive-fonts-extra
  ```


#### Instalación automática con script
Para instalar todo automáticamente, usa el script `install.sh`:
```bash
chmod +x install.sh
./install.sh
```

---

## Uso de la aplicación

### 1. Preparar los archivos
- Asegúrate de tener archivos CSV con los eventos. **Cada CSV se convertirá en una tabla en SQLite con el mismo nombre del archivo.**
- Las imágenes deben estar en la carpeta de imágenes y nombradas según el mes: `enero.jpeg`, `febrero.jpeg`, etc.

### 2. Ejecutar la aplicación
Inicia la interfaz de Streamlit con:
```bash
streamlit run app.py
```
O bien, usa el script de inicio `start.sh`:
```bash
chmod +x start.sh
./start.sh
```
Esto abrirá la aplicación en tu navegador.

### 3. Gestionar eventos
Desde la interfaz puedes:
- **Cargar eventos** desde los archivos CSV
- **Agregar, modificar y eliminar eventos** en la base de datos SQLite

### 4. Exportar el calendario a LaTeX y PDF
- Presiona el botón **"Exportar a LaTeX"** para generar el archivo `.tex`
- Presiona **"Compilar PDF"** para generar el calendario en formato PDF

---

## Uso con Docker

PhotoCalendar incluye un `Dockerfile` y un archivo `docker-compose.yml` para facilitar la implementación en contenedores.

### Construir la imagen Docker
Si deseas crear la imagen de la aplicación localmente, ejecuta:
```bash
docker build -t photocalendar .
```

### Ejecutar la aplicación desde Docker Hub
Si ya has subido tu imagen a Docker Hub, puedes ejecutarla directamente con:
```bash
docker run -d -p 8501:8501 -v ./output:/app/output -v ./input/:/app/input -v ./images/:/app/images andresmarinabad24/photocalendar
```
Esto iniciará la aplicación y podrás acceder a ella en `http://localhost:8501`.

Añade un volumen en /app/data para que la base de datos sea persistente:
```commandline
-v ./data:/app/data
```

### Ejecutar con Docker Compose
Para ejecutar con `docker-compose`, usa:
```bash
docker-compose up -d
```

### Resultado 
El PDF de salida se almacena en el volumen output como: *calendar.pdf*

---

## Estructura del Proyecto
```bash
├── build
│   ├── calendar.sty
│   └── calendar.tex
├── data
│   ├── data.csv
│   └── data.db
├── LICENSE
├── README.md
├── src
│   ├── config.py
│   ├── database.py
│   ├── data.py
│   ├── __init__.py
│   ├── app.py
│   ├── render.py
│   ├── template
│   │   └── plantilla_imagen.xcf
│   └── utils.py
├── templates
│   └── header
├── install.sh
├── start.sh
├── Dockerfile
└── docker-compose.yml
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




