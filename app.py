from flask import Flask, render_template, request, jsonify
from rules import evaluar_proyecto  # Importa la función desde el archivo rules.py

# Crea la aplicación Flask
app = Flask(__name__)

# Ruta principal: muestra el formulario HTML
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para evaluar los datos enviados desde el frontend (JS)
@app.route("/evaluate", methods=["POST"])
def evaluate():
    # Recibe los datos JSON del frontend
    datos = request.get_json()

    # Llama a la función del motor de reglas
    total_puntos, retroalimentacion = evaluar_proyecto(datos)

    # Devuelve los resultados al frontend como JSON
    return jsonify({
        "totalPuntos": total_puntos,
        "retroalimentacion": retroalimentacion
    })

# Ejecuta la app en modo desarrollo si se llama directamente
if __name__ == "__main__":
    app.run(debug=True)
