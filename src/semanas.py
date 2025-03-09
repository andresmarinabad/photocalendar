import calendar

def tiene_muchas_semanas(anio, mes):
    """
    Calcula cuántas semanas tiene un mes y determina si tiene más de lo normal (6 semanas).
    
    Args:
        anio (int): Año en formato YYYY.
        mes (int): Mes (1-12).
        
    Returns:
        tuple: (num_semanas, bool) -> Número de semanas y True si tiene 6 semanas, False si tiene 4-5.
    """
    # Obtener el primer y último día del mes
    primer_dia, num_dias = calendar.monthrange(anio, mes)
    
    # Calcular la primera y última semana del mes
    primera_semana = (1 + primer_dia) // 7  # Semana donde cae el día 1
    ultima_semana = (num_dias + primer_dia) // 7  # Semana donde cae el último día

    # Calcular el número total de semanas únicas en el mes
    semanas = ultima_semana - primera_semana + 1
    
    return semanas, semanas == 6

# 📌 Ejemplo: Marzo 2024
print(tiene_muchas_semanas(2024, 3))  # (6, True)
print(tiene_muchas_semanas(2024, 4))  # (5, False)