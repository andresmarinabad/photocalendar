import datetime
import dateutil.easter
import ephem
import os
import glob
import calendar
import subprocess
import shutil

from .config import config

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}


def _add_event(fecha: datetime.date, nombre: str, eventos: dict) -> None:
    mes = MESES[fecha.month]
    eventos.setdefault(mes, {})[fecha.day] = nombre


def ciclo_liturgico(year: int) -> str:
    if year % 3 == 0:
        return "C"
    elif year % 3 == 1:
        return "A"
    else:
        return "B"


def calcular_eventos_calendario(year: int) -> dict:
    """Festivos y fechas astronómicas para el año dado."""
    eventos: dict = {}

    pascua = dateutil.easter.easter(year)
    _add_event(pascua - datetime.timedelta(days=7), "{\\color{red} Ramos}", eventos)
    _add_event(pascua, "{\\color{red} Pascua}", eventos)
    _add_event(pascua - datetime.timedelta(days=3), "{\\color{red} Jueves Santo}", eventos)
    _add_event(pascua - datetime.timedelta(days=2), "{\\color{red} Viernes Santo}", eventos)
    _add_event(pascua - datetime.timedelta(days=46), "{\\color{Purple} Ceniza}", eventos)
    _add_event(pascua + datetime.timedelta(days=49), "{\\color{red} Pentecostés}", eventos)

    ultimo_dom_marzo = max(
        datetime.date(year, 3, d) for d in range(25, 32)
        if datetime.date(year, 3, d).weekday() == 6
    )
    ultimo_dom_oct = max(
        datetime.date(year, 10, d) for d in range(25, 32)
        if datetime.date(year, 10, d).weekday() == 6
    )
    _add_event(ultimo_dom_marzo, "Horario verano \\showclock{3}{00}", eventos)
    _add_event(ultimo_dom_oct, "Horario invierno \\showclock{2}{00}", eventos)

    _add_event(ephem.localtime(ephem.next_vernal_equinox(str(year))).date(), "{\\color{Lavender} Primavera}", eventos)
    _add_event(ephem.localtime(ephem.next_summer_solstice(str(year))).date(), "{\\color{Emerald} Verano}", eventos)
    _add_event(ephem.localtime(ephem.next_autumnal_equinox(str(year))).date(), "{\\color{Orange} Otoño}", eventos)
    _add_event(ephem.localtime(ephem.next_winter_solstice(str(year))).date(), "{\\color{Cyan} Invierno}", eventos)

    primer_dom_adviento = next(
        datetime.date(year, m, d)
        for m, d in ((11, 27), (11, 28), (11, 29), (11, 30), (12, 1), (12, 2), (12, 3))
        if datetime.date(year, m, d).weekday() == 6
    )
    ciclo = ciclo_liturgico(year + 1)
    _add_event(primer_dom_adviento, f"{{\\color{{Plum}} Adviento I ({ciclo})}}", eventos)

    festivos = [
        ((1, 1),  "{\\color{SkyBlue} Santa María Madre de Dios}"),
        ((1, 6),  "{\\color{PineGreen} La Epifanía}"),
        ((5, 1),  "Día del trabajo"),
        ((6, 23), "{\\color{CadetBlue} Verbena de San Juan}"),
        ((8, 15), "{\\color{SkyBlue} La Asunción}"),
        ((9, 11), "Diada de Cataluña"),
        ((9, 24), "{\\color{Peach} La Mercè}"),
        ((10, 12), "{\\color{VioletRed} Nuestra Señora del Pilar}"),
        ((11, 1), "{\\color{OrangeRed} Todos los Santos}"),
        ((11, 2), "{\\color{Brown} Fieles difuntos}"),
        ((12, 6), "La Constitución"),
        ((12, 8), "{\\color{SkyBlue} La Inmaculada}"),
        ((12, 25), "{\\color{red} Navidad}"),
        ((12, 26), "{\\color{RubineRed} San Esteban}"),
    ]
    for (m, d), label in festivos:
        _add_event(datetime.date(year, m, d), label, eventos)

    return eventos


def consultar_leyenda(titulo: str, opciones: str, year: int) -> str:
    try:
        birth_year = int(opciones)
        return f"{titulo} {year - birth_year}"
    except ValueError:
        if opciones == "memoria":
            return f"{titulo} \\Cross"
        return titulo


def _celdas_mes(year: int, mes: int) -> int:
    primer_dia, num_dias = calendar.monthrange(year, mes)
    return ((primer_dia + num_dias + 6) // 7) * 7


def _get_month_image(mes_nombre: str) -> str:
    images_path = os.path.join(config.ROOT, "images")
    matches = glob.glob(os.path.join(images_path, f"{mes_nombre}.*"))
    return matches[0] if matches else "example-image"


def load_all_days(events: list[dict], year: int) -> dict:
    """Construye el diccionario clave→LaTeX para todos los días del año."""
    eventos_cal = calcular_eventos_calendario(year)

    events_by_day: dict[str, list[dict]] = {}
    for ev in events:
        events_by_day.setdefault(f"{ev['mes']}{ev['dia']}", []).append(ev)

    todos_dias: dict[str, str] = {}
    for mes_num in range(1, 13):
        mes = MESES[mes_num]
        _, ndias = calendar.monthrange(year, mes_num)
        for dia in range(1, ndias + 1):
            clave = f"{mes}{dia}"
            fiesta = eventos_cal.get(mes, {}).get(dia, "")
            este_dia = ""
            for ev in events_by_day.get(clave, []):
                text = consultar_leyenda(ev["titulo"], ev["opciones"], year)
                este_dia = f"{este_dia}\\\\{text}" if este_dia else text
            todos_dias[clave] = f"\\day{{{fiesta}}}{{\\vspace{{1.75cm}}{este_dia}}}\n"

    return todos_dias


def create_calendar_tex(days: dict, year: int) -> None:
    header_path = os.path.join(config.ROOT, "templates", "header")
    with open(header_path) as f:
        header = f.read()

    build_path = os.path.join(config.ROOT, "build", "calendar.tex")
    with open(build_path, "w", encoding="utf-8") as c:
        c.write(header)

        for mes in range(1, 13):
            mes_nombre = MESES[mes]
            image = _get_month_image(mes_nombre)

            c.write("\n\\begin{figure*}[t!]\n\\begin{center}\n")
            c.write(f"\\includegraphics[width=\\linewidth]{{{image}}}\n")
            c.write("\\end{center}\n\\end{figure*}\n")
            c.write("\\begin{center}\n")
            c.write(f"\\textsc{{\\LARGE {mes_nombre.upper()}}}\\ % Month\n")
            c.write(f"\\textsc{{\\LARGE {year}}} % Year\n")
            c.write("\\end{center}\n\n")
            c.write("\\begin{calendar}{\\textwidth}\n")

            primer_dia, count_days = calendar.monthrange(year, mes)
            counter = 1 - primer_dia
            c.write(f"\\setcounter{{calendardate}}{{{counter}}}\n")

            for _ in range(_celdas_mes(year, mes)):
                if counter < 1 or counter > count_days:
                    c.write("\\BlankDay\n")
                else:
                    clave = f"{mes_nombre}{counter}"
                    c.write(days.get(clave, "\\day{}{\\vspace{1.75cm}}\n"))
                counter += 1

            c.write("\\finishCalendar\n\\end{calendar}\n\\newpage")

        c.write("\\end{document}")


def compile_pdf(calendar_name: str) -> str:
    """Compila el .tex y deja el PDF en output/{calendar_name}.pdf. Devuelve la ruta."""
    build_dir = os.path.join(config.ROOT, "build")
    result = subprocess.run(
        "pdflatex -interaction=nonstopmode calendar.tex",
        shell=True,
        cwd=build_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log = (result.stdout or "") + "\n" + (result.stderr or "")
        raise RuntimeError(f"pdflatex falló:\n{log[-3000:]}")

    src = os.path.join(build_dir, "calendar.pdf")
    dst = os.path.join(config.OUTPUT_PATH, f"{calendar_name}.pdf")
    shutil.move(src, dst)
    return dst
