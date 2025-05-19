from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Ponderaciones por actividad
ponderaciones = {
    'presentacion': 5,
    'descripcion': 5,
    'explicacion': 30,
    'manejo': 15,
    'resolucion': 15,
    'contacto_visual': 5,
    'tono_voz': 5,
    'organizacion': 5,
    'responde_preguntas': 10,
    'tiempo': 5,
}

actividades_texto = {
    'presentacion': '1. Presentación de cada integrante (Nombre completo).',
    'descripcion': '2. Descripción del proyecto de manera clara.',
    'explicacion': '3. Explicación detallada de los componentes del proyecto.',
    'manejo': '4. Manejo adecuado de los recursos y herramientas.',
    'resolucion': '5. Resolución de problemas durante la exposición.',
    'contacto_visual': '6. Contacto visual adecuado con la audiencia.',
    'tono_voz': '7. Tono de voz adecuado durante la exposición.',
    'organizacion': '8. Organización y estructura de la exposición.',
    'responde_preguntas': '9. Responde adecuadamente a las preguntas de la audiencia.',
    'tiempo': '10. Cumple con el tiempo asignado para la presentación.',
}

@app.route('/')
def index():
    return render_template('index.html', ponderaciones=ponderaciones, actividades_texto=actividades_texto)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    total_puntos = 0
    detalles = {}

    for clave, info in data.items():
        cumplido = info.get('cumplido', False)
        puntos = int(info.get('puntos', 0)) if info.get('puntos', '').isdigit() else 0
        retroalimentacion = info.get('retroalimentacion', '').strip()

        if not cumplido:
            puntos = 0  # Si no cumplido, no se suma puntaje

        max_puntos = ponderaciones.get(clave, 0)
        # Limitar el puntaje al máximo permitido
        if puntos > max_puntos:
            puntos = max_puntos

        total_puntos += puntos
        detalles[clave] = {
            'actividad': actividades_texto.get(clave, clave),
            'retroalimentacion': retroalimentacion,
        }

    return jsonify({
        'totalPuntos': total_puntos,
        'detalles': detalles
    })

if __name__ == '__main__':
    app.run(debug=True)
