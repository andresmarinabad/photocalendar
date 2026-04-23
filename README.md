# PhotoCalendar

Aplicación en Python con **Streamlit** para gestionar un calendario fotográfico personalizado: importa CSV a **SQLite**, edita eventos en la web y genera un **PDF** vía **LaTeX** (`pdflatex`).

---

![Python](https://img.shields.io/badge/python-3.12+-green)
![Streamlit](https://img.shields.io/badge/ui-streamlit-orange)
![LaTeX](https://img.shields.io/badge/pdf-pdflatex-blue)
![uv](https://img.shields.io/badge/deps-uv-905eff)

## Requisitos

- [Nix](https://nixos.org/) con flakes (el entorno del `flake.nix` incluye **uv**, **TeX Live completo** y **sqlite** en el `PATH`).
- Opcional: [direnv](https://direnv.net/) + [nix-direnv](https://github.com/nix-community/nix-direnv) — el repositorio incluye `.envrc` con `use flake` para entrar al shell al abrir la carpeta.

## Puesta en marcha

```bash
nix develop
uv sync
uv run streamlit run src/app.py
```

## Año del calendario

Por defecto se usa **el año siguiente al actual** (comportamiento pensado para imprimir el calendario del año que viene). Puedes fijar el año con la variable de entorno `YEAR` (debe ser un entero):

```bash
YEAR=2026 uv run streamlit run src/app.py
```

Al generar el PDF, febrero y los meses de 30/31 días respetan ese año (incluidos bisiestos).

## Uso

1. Coloca CSV en `input/` con columnas `dia`, `titulo`, `opciones`, `mes` (nombre del mes en minúsculas, en español: `enero`, `febrero`, …). El nombre del archivo define la tabla en SQLite.
2. Imágenes por mes en `images/`, por ejemplo `enero.jpeg`, `febrero.png`, etc.
3. En la interfaz: carga datos, edita y pulsa **Crear Calendario**; el PDF queda en `output/calendar.pdf` (requiere `pdflatex` en el PATH, provisto por el flake).

## Estructura del proyecto

```text
├── build/           # calendar.sty y calendar.tex generado
├── data/            # SQLite (p. ej. data.db)
├── images/          # Fotos por mes
├── input/           # CSV de entrada
├── output/          # calendar.pdf
├── src/             # app Streamlit, utilidades, BD
├── templates/header
├── flake.nix
├── pyproject.toml
└── uv.lock
```

## Licencia

MIT.
