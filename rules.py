def evaluar_proyecto(datos):
    ponderaciones = {
        "presentacion": 5,
        "descripcion": 5,
        "explicacion": 30,
        "manejo": 15,
        "resolucion": 15,
        "contacto_visual": 5,
        "tono_voz": 5,
        "organizacion": 5,
        "responde_preguntas": 10,
        "tiempo": 5
    }

    total_puntos = 0
    detalles = {}

    for actividad, max_puntos in ponderaciones.items():
        actividad_data = datos.get(actividad, {})
        cumplido = actividad_data.get("cumplido", False)
        puntaje = int(actividad_data.get("puntos", 0)) if cumplido else 0
        if puntaje > max_puntos:
            puntaje = max_puntos

        detalles[actividad] = {
            "actividad": actividad.replace('_', ' ').capitalize(),
            "puntos": puntaje,
            "retroalimentacion": actividad_data.get("retroalimentacion", "")
        }

        total_puntos += puntaje

    return total_puntos, detalles
