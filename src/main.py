YEAR = 2025

from datetime import datetime
import os
import shutil
import csv


def extract_from_csv(month_file, month_obj):
    with open(month_file, newline='', encoding='utf-8') as enero:
        data_enero = csv.DictReader(enero)

        for row in data_enero:
            try:
                year = int(row['notas'])
                if int(row['dia']) not in month_obj:
                    month_obj[int(row['dia'])] = row['info'] + f' {YEAR - year}'
                else:
                    month_obj[int(row['dia'])] = \
                        month_obj[int(row['dia'])] \
                        + '\\\\' + row['info'] + f' {YEAR - year}'
            except ValueError:
                # santo u otra cosa
                if int(row['dia']) not in month_obj:
                    month_obj[int(row['dia'])] = row['info']
                else:
                    month_obj[int(row['dia'])] = \
                        month_obj[int(row['dia'])] + '\\\\' + row['info']


if __name__ == '__main__':

    with open('../templates/header') as h:
        header = h.readlines()

    # ENERO
    uno_enero = datetime.strptime(f'0101{YEAR}', "%d%m%Y").date()
    fechas_enero = {}
    extract_from_csv('../data/enero.csv', fechas_enero)

    with open('../build/calendar.tex', 'w', encoding='utf-8') as c:
        for line in header:
            c.write(line)

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Enero}\\ % Month\n")
        c.write("\\textsc{\LARGE "+f"{YEAR}"+"} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_enero.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{"+f"{counter}"+"}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 42):
            counter +=1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2cm}}\n"

            if counter-1 in fechas_enero:
                c.write("\day{}{\\vspace{1.5cm}"+fechas_enero[counter-1]+"}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # FEBRERO
    uno_febrero = datetime.strptime(f'0102{YEAR}', "%d%m%Y").date()
    fechas_febrero = {}
    extract_from_csv('../data/febrero.csv', fechas_febrero)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Febrero}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_febrero.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 28:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 28
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_febrero:
                c.write("\day{}{\\vspace{2cm}" + fechas_febrero[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")

    # MARZO
    uno_marzo = datetime.strptime(f'0103{YEAR}', "%d%m%Y").date()
    fechas_marzo = {}
    extract_from_csv('../data/marzo.csv', fechas_marzo)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Marzo}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_marzo.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_marzo:
                c.write("\day{}{\\vspace{2cm}" + fechas_marzo[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # ABRIL
    uno_abril = datetime.strptime(f'0104{YEAR}', "%d%m%Y").date()
    fechas_abril = {}
    extract_from_csv('../data/abril.csv', fechas_abril)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Abril}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_abril.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 30:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 30
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_abril:
                c.write("\day{}{\\vspace{2cm}" + fechas_abril[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # MAYO
    uno_mayo = datetime.strptime(f'0105{YEAR}', "%d%m%Y").date()
    fechas_mayo = {}
    extract_from_csv('../data/mayo.csv', fechas_mayo)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Mayo}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_mayo.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_mayo:
                c.write("\day{}{\\vspace{2cm}" + fechas_mayo[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # JUNIO
    uno_junio = datetime.strptime(f'0106{YEAR}', "%d%m%Y").date()
    fechas_junio = {}
    extract_from_csv('../data/junio.csv', fechas_junio)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Junio}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_junio.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 30:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 30
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_junio:
                c.write("\day{}{\\vspace{2cm}" + fechas_junio[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # JULIO
    uno_julio = datetime.strptime(f'0107{YEAR}', "%d%m%Y").date()
    fechas_julio = {}
    extract_from_csv('../data/julio.csv', fechas_julio)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Julio}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_julio.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 42):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2cm}}\n"

            if counter - 1 in fechas_julio:
                c.write("\day{}{\\vspace{1.5cm}" + fechas_julio[counter - 1] + "}\n")
                # \day{}{\vspace{2cm}} si es primero de semana y ultimo de mes
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # AGOSTO
    uno_agosto = datetime.strptime(f'0108{YEAR}', "%d%m%Y").date()
    fechas_agosto = {}
    extract_from_csv('../data/agosto.csv', fechas_agosto)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Agosto}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_agosto.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_agosto:
                c.write("\day{}{\\vspace{2cm}" + fechas_agosto[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")

    # SEPTIEMBRE
    uno_septiembre = datetime.strptime(f'0109{YEAR}', "%d%m%Y").date()
    fechas_septiembre = {}
    extract_from_csv('../data/septiembre.csv', fechas_septiembre)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Septiembre}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_septiembre.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 30:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 30
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_septiembre:
                c.write("\day{}{\\vspace{2cm}" + fechas_septiembre[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")


    # OCUTBRE
    uno_octubre = datetime.strptime(f'0110{YEAR}', "%d%m%Y").date()
    fechas_octubre = {}
    extract_from_csv('../data/octubre.csv', fechas_octubre)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Octubre}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_octubre.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 42):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2cm}}\n"

            if counter - 1 in fechas_octubre:
                c.write("\day{}{\\vspace{1.5cm}" + fechas_octubre[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")



    # NOVIEMBRE
    uno_noviembre = datetime.strptime(f'0111{YEAR}', "%d%m%Y").date()
    fechas_noviembre = {}
    extract_from_csv('../data/noviembre.csv', fechas_noviembre)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Noviembre}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_noviembre.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 30:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 30
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_noviembre:
                c.write("\day{}{\\vspace{2cm}" + fechas_noviembre[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")



    # DICIEMBRE
    uno_diciembre = datetime.strptime(f'0112{YEAR}', "%d%m%Y").date()
    fechas_diciembre = {}
    extract_from_csv('../data/diciembre.csv', fechas_diciembre)

    with open('../build/calendar.tex', 'a', encoding='utf-8') as c:

        c.write("\n")
        c.write("\\begin{figure*}[t!]\n")
        c.write("\\begin{center}\n")
        c.write("\includegraphics[width=\linewidth]{example-image}\n")
        c.write("\end{center}\n")
        c.write("\end{figure*}\n")

        c.write("\\begin{center}\n")
        c.write("\\textsc{\LARGE Diciembre}\\ % Month\n")
        c.write("\\textsc{\LARGE " + f"{YEAR}" + "} % Year\n")
        c.write("\end{center}\n\n")

        c.write("\\begin{calendar}{\\textwidth}\n")

        dia_semana = uno_diciembre.weekday()
        counter = (dia_semana - 1) * (-1)
        c.write("\setcounter{calendardate}{" + f"{counter}" + "}\n")
        to_write = "\BlankDay\n"
        for day in range(0, 35):
            counter += 1
            if dia_semana == day:
                if day >= 31:
                    to_write = "\BlankDay\n"
                    dia_semana = 100
                else:
                    dia_semana = dia_semana + 31
                    to_write = "\day{}{\\vspace{2.5cm}}\n"

            if counter - 1 in fechas_diciembre:
                c.write("\day{}{\\vspace{2cm}" + fechas_diciembre[counter - 1] + "}\n")
                continue

            c.write(to_write)

        c.write("\\finishCalendar\n")
        c.write("\end{calendar}\n")

        # END CALENDAR
        c.write("\end{document}")


    # COMPILE
    calendar_tex = '../build/calendar.tex'
    calendar_new = '../build/calendar.pdf'
    calendar_mv = '../output/calendar.pdf'

    #os.system(f"pdflatex -quiet {calendar_tex}")
    #shutil.move(calendar_new, calendar_mv)