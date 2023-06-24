from flask import Flask, render_template, request
import pandas as pd
from geopy import distance

app = Flask(__name__)

def calcular_distancia(aeropuerto1, aeropuerto2, df):
    coordenadas_aeropuerto1 = (df.loc[df['Nombre'] == aeropuerto1, 'Latitud'].values[0],
                            df.loc[df['Nombre'] == aeropuerto1, 'Longitud'].values[0])
    
    coordenadas_aeropuerto2 = (df.loc[df['Nombre'] == aeropuerto2, 'Latitud'].values[0],
                            df.loc[df['Nombre'] == aeropuerto2, 'Longitud'].values[0])
    
    return distance.distance(coordenadas_aeropuerto1, coordenadas_aeropuerto2).kilometers


@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_excel('Aeropuertos.xlsx', sheet_name='Aeropuertos')
    aeropuertos = df['Nombre'].tolist()
    
    ruta_encontrada = None
    
    if request.method == 'POST':
        aeropuerto_origen = request.form['aeropuerto_origen']
        aeropuerto_destino = request.form['aeropuerto_destino']
        
        distancia_minima = calcular_distancia(aeropuerto_origen, aeropuerto_destino, df)
        ruta_encontrada = f"La distancia más corta entre {aeropuerto_origen} y {aeropuerto_destino} es {distancia_minima} km."
    
        return ruta_encontrada
    
    return render_template('form.html', ruta_encontrada=ruta_encontrada, aeropuertos=aeropuertos)
