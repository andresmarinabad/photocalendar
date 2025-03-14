import datetime
import dateutil.easter
import ephem
import os
import glob
import calendar
import subprocess
from config import config

# Diccionario de nombres de los meses en castellano
MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def obtener_fecha_diccionario(fecha, nombre_evento, eventos):
    """Añade un evento al diccionario en el formato requerido."""
    mes = MESES[fecha.month]
    dia = fecha.day
    if mes not in eventos:
        eventos[mes] = {}
    eventos[mes][dia] = nombre_evento

def calcular_eventos_calendario():
    """Calcula fechas clave del calendario y las devuelve organizadas por mes."""
    
    año = config.YEAR
    eventos = {}  # Diccionario de eventos organizado por mes

    # Pascua y días relacionados
    pascua = dateutil.easter.easter(año)
    ramos = pascua - datetime.timedelta(days=7)
    jueves_santo = pascua - datetime.timedelta(days=3)
    viernes_santo = pascua - datetime.timedelta(days=2)
    miércoles_ceniza = pascua - datetime.timedelta(days=46)  # 46 días antes de Pascua
    pentecostes = pascua + datetime.timedelta(days=49)  # 49 días después de Pascua
    
    # Cambio de hora en España (últimos domingos de marzo y octubre)
    ultimo_domingo_marzo = max(
        datetime.date(año, 3, d) for d in range(25, 32) if datetime.date(año, 3, d).weekday() == 6
    )
    ultimo_domingo_octubre = max(
        datetime.date(año, 10, d) for d in range(25, 32) if datetime.date(año, 10, d).weekday() == 6
    )

    # Solsticios y equinoccios con ephem
    primavera = ephem.localtime(ephem.next_vernal_equinox(str(año)))
    verano = ephem.localtime(ephem.next_summer_solstice(str(año)))
    otoño = ephem.localtime(ephem.next_autumnal_equinox(str(año)))
    invierno = ephem.localtime(ephem.next_winter_solstice(str(año)))

    # Primer Domingo de Adviento (cuarto domingo antes de Navidad)
    primer_domingo_adviento = max(
        datetime.date(año, 11, d) for d in range(27, 31) if datetime.date(año, 11, d).weekday() == 6
    )

    epifania = datetime.date(año, 1, 6)
    uno_enero = datetime.date(año, 1, 1)
    navidad = datetime.date(año, 12, 25)
    esteban = datetime.date(año, 12, 26)
    consti = datetime.date(año, 12, 6)
    inmaculada = datetime.date(año, 12, 8)
    santos = datetime.date(año, 11, 1)
    difuntos = datetime.date(año, 11, 2)
    trabajo = datetime.date(año, 5, 1)
    verbena = datetime.date(año, 6, 23)
    diada = datetime.date(año, 9, 11)
    merce = datetime.date(año, 9, 24)
    pilar = datetime.date(año, 10, 12)
    asuncion = datetime.date(año, 8, 15)

    # Agregar eventos al diccionario
    obtener_fecha_diccionario(ramos, "{\\color{red} Ramos}", eventos)
    obtener_fecha_diccionario(pascua, "{\\color{red} Pascua}", eventos)
    obtener_fecha_diccionario(jueves_santo, "{\\color{red} Jueves Santo}", eventos)
    obtener_fecha_diccionario(viernes_santo, "{\\color{red} Viernes Santo}", eventos)
    obtener_fecha_diccionario(miércoles_ceniza, "{\\color{Purple} Ceniza}", eventos)
    obtener_fecha_diccionario(pentecostes, "{\\color{red} Pentecostés}", eventos)
    obtener_fecha_diccionario(ultimo_domingo_marzo, "Horario verano \\showclock{3}{00}", eventos)
    obtener_fecha_diccionario(ultimo_domingo_octubre, "Horario invierno \\showclock{2}{00}", eventos)
    obtener_fecha_diccionario(verano, "{\\color{Emerald} Verano}", eventos)
    obtener_fecha_diccionario(primavera, "{\\color{Lavender} Primavera}", eventos)
    obtener_fecha_diccionario(otoño, "{\\color{Orange} Otoño}", eventos)
    obtener_fecha_diccionario(invierno, "{\\color{Cyan} Invierno}", eventos)
    ciclo = ciclo_liturgico(config.YEAR+1)
    obtener_fecha_diccionario(primer_domingo_adviento, "{\\color{Plum} Adviento I ("+ciclo+")}", eventos)
    obtener_fecha_diccionario(epifania, "{\\color{PineGreen} La Epifanía}", eventos)
    obtener_fecha_diccionario(uno_enero, "{\\color{SkyBlue} Santa María Madre de Dios}", eventos)
    obtener_fecha_diccionario(navidad, "{\\color{red} Navidad}", eventos)
    obtener_fecha_diccionario(esteban, "{\\color{RubineRed} San Esteban}", eventos)
    obtener_fecha_diccionario(consti, "La Constitución", eventos)
    obtener_fecha_diccionario(inmaculada, "{\\color{SkyBlue} La Inmaculada}", eventos)
    obtener_fecha_diccionario(santos, "{\\color{OrangeRed} Todos los Santos}", eventos)
    obtener_fecha_diccionario(difuntos, "{\\color{Brown} Fieles difuntos}", eventos)
    obtener_fecha_diccionario(trabajo, "Día del trabajo", eventos)
    obtener_fecha_diccionario(verbena, "{\\color{CadetBlue} Verbena de San Juan}", eventos)
    obtener_fecha_diccionario(diada, "Diada de Cataluña", eventos)
    obtener_fecha_diccionario(merce, "{\\color{Peach} La Mercè}", eventos)
    obtener_fecha_diccionario(pilar, "{\\color{VioletRed} Nuestra Señora del Pilar}", eventos)
    obtener_fecha_diccionario(asuncion, "{\\color{SkyBlue} La Asunción}", eventos)

    return eventos

def calcula_num_semanas(anio, mes):

    primer_dia, num_dias = calendar.monthrange(anio, mes)
    primera_semana = (1 + primer_dia) // 7 
    ultima_semana = (num_dias + primer_dia) // 7 
    ultimo_dia_semana = (primer_dia + num_dias - 1) % 7
    semanas = ultima_semana - primera_semana + 1
    if ultimo_dia_semana == 6:
        semanas -= 1
    
    return semanas

def es_bisiesto(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def dias_en_mes(mes):
    mes_num = next((k for k, v in MESES.items() if v == mes), None)
    return calendar.monthrange(config.YEAR, mes_num)[1]


def consultar_leyenda(titulo, opciones):
    try:
        cumple = int(opciones)
        num = config.YEAR - cumple
        return f'{titulo} {num}'
    except ValueError:
        if opciones == 'memoria':
            return f'{titulo} \\Cross'
        else:
            return f'{titulo}'


def ciclo_liturgico(anio):
    if anio % 3 == 0:
        return "C"
    elif anio % 3 == 1:
        return "A"
    else:
        return "B"


def compile_pdf():
    build_path = os.path.join(config.ROOT, 'build')
    subprocess.run(f"cd {build_path} && pdflatex calendar.tex && mv calendar.pdf ../output/calendar.pdf", shell=True, check=True)
    return True

def get_month_image(mes):
    images_path = os.path.join(config.ROOT, 'images')
    imagen = glob.glob(os.path.join(images_path, f"{mes}.*"))
    if len(imagen) > 0:
        return imagen[0]
    return 'example-image'
    

def create_calendar_tex(days):
    header_path = os.path.join(config.ROOT, 'templates', 'header')
    with open(header_path) as h:
        header = h.read()

    build_path = os.path.join(config.ROOT, 'build', 'calendar.tex')
    with open(build_path, 'w', encoding='utf-8') as c:
        c.write(header)
    
        for mes in range(1, 13):

            c.write("\n")
            c.write("\\begin{figure*}[t!]\n")
            c.write("\\begin{center}\n")
            image = get_month_image(MESES[mes])
            c.write("\\includegraphics[width=\\linewidth]{"+image+"}\n")
            c.write("\\end{center}\n")
            c.write("\\end{figure*}\n")
            c.write("\\begin{center}\n")
            c.write("\\textsc{\\LARGE "+MESES[mes].upper()+"}\\ % Month\n")
            c.write("\\textsc{\\LARGE "+f"{config.YEAR}"+"} % Year\n")
            c.write("\\end{center}\n\n")
            c.write("\\begin{calendar}{\\textwidth}\n")

            primer_dia, count_days = calendar.monthrange(config.YEAR, mes)
            counter = 1 - primer_dia
            
            c.write("\\setcounter{calendardate}{"+str(counter)+"}\n")
            to_write = "\\BlankDay\n"
            max_range = calcula_num_semanas(config.YEAR, mes) * 7
            max_range = max_range if primer_dia != 6 else max_range + 7
            for day in range(0, max_range):
                if counter < 1 or counter > count_days:
                    to_write = "\\BlankDay\n"
                else:
                    to_write = "\\day{}{\\vspace{1.75cm}}\n"
                
                mes_str = MESES[mes]
                clave = f'{mes_str}{counter}'
                if clave in days:
                    to_write = days[clave]
                
                c.write(to_write)
                counter += 1 

            c.write("\\finishCalendar\n")
            c.write("\\end{calendar}\n")
            c.write("\\newpage")
        c.write("\\end{document}")

                    
