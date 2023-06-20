from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', ruta_encontrada=None)

@app.route('/ruta', methods=['POST'])
def buscar_ruta():
    aeropuerto_origen = request.form['aeropuerto_origen']
    aeropuerto_destino = request.form['aeropuerto_destino']
    # Aquí puedes realizar la lógica para buscar la ruta más corta entre los aeropuertos
    # y almacenar la ruta encontrada en una variable
    # Por ahora, solo imprimiremos los aeropuertos en la consola
    print(f"Aeropuerto de origen: {aeropuerto_origen}")
    print(f"Aeropuerto de destino: {aeropuerto_destino}")
    
    # Ejemplo de ruta encontrada
    ruta_encontrada = f"{aeropuerto_origen} -> {aeropuerto_destino} -> {aeropuerto_origen}"
    
    return render_template('form.html', ruta_encontrada=ruta_encontrada)

if __name__ == '__main__':
    app.run()

