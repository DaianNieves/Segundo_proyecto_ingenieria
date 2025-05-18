def evaluar_proyecto(datos):
    """
    Evalúa el proyecto según las actividades y retorna el puntaje total
    y una retroalimentación detallada.

    :param datos: dict con claves (nombres de actividades) y valores booleanos
                  indicando si la actividad fue cumplida (True) o no (False).
                  Por ejemplo:
                  {
                    "presentacion": True,
                    "descripcion": False,
                    ...
                  }
    :return: tuple (total_puntos: int, retroalimentacion: str)
             total_puntos: suma de los puntos obtenidos según las actividades cumplidas
             retroalimentacion: texto que detalla qué actividades se cumplieron y cuáles no,
                                y la evaluación final (aprobado/no aprobado)
    """

    # Diccionario con las actividades y los puntos asignados a cada una
    actividades = {
        "presentacion": 5,
        "descripcion": 5,
        "explicacion": 30,
        "manejo": 15,
        "resolucion": 15,
        "contacto_visual": 5,
        "tono_voz": 5,
        "organizacion": 5,
        "responde_preguntas": 10,
        "tiempo": 5,
    }

    total_puntos = 0  # Inicializa el contador de puntos acumulados
    retroalimentacion = []  # Lista para almacenar mensajes de retroalimentación

    # Recorre cada actividad para evaluar si fue cumplida o no
    for actividad, puntos in actividades.items():
        if datos.get(actividad, False):  # Si la actividad está en datos y es True
            total_puntos += puntos  # Suma los puntos correspondientes
            # Agrega mensaje positivo para la actividad cumplida
            retroalimentacion.append(f"✅ {actividad.replace('_', ' ').capitalize()} cumplido (+{puntos} puntos)")
        else:
            # Mensaje negativo si la actividad no fue cumplida o no está presente en datos
            retroalimentacion.append(f"❌ {actividad.replace('_', ' ').capitalize()} no cumplido (0 puntos)")

    # Añade mensaje final según si se alcanza o no el puntaje mínimo aprobatorio (70)
    if total_puntos >= 70:
        retroalimentacion.append("\nEvaluación: Proyecto aprobado")
    else:
        retroalimentacion.append("\nEvaluación: Proyecto no aprobado")

    # Devuelve el puntaje total y la retroalimentación como un solo string separado por saltos de línea
    return total_puntos, "\n".join(retroalimentacion)
