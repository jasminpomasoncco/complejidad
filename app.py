from flask import Flask, render_template, request
import pandas as pd
from geopy import distance
import math
import heapq
import numpy as np

app = Flask(__name__)

def calcular_distancias_floyd_warshall(df):
    num_aeropuertos = len(df)
    
    # Crear una matriz de distancias inicializada con infinito para todos los pares de aeropuertos
    distancias = np.full((num_aeropuertos, num_aeropuertos), np.inf)
    
    # Llenar la matriz de distancias con las distancias conocidas entre aeropuertos
    for i, row in df.iterrows():
        aeropuerto1 = row['Nombre']
        coordenadas_aeropuerto1 = (row['Latitud'], row['Longitud'])
        for j, neighbor_row in df.iterrows():
            if i != j:
                aeropuerto2 = neighbor_row['Nombre']
                coordenadas_aeropuerto2 = (neighbor_row['Latitud'], neighbor_row['Longitud'])
                distancia = distance.distance(coordenadas_aeropuerto1, coordenadas_aeropuerto2).kilometers
                distancias[i, j] = distancia
    
    # Algoritmo de Floyd-Warshall
    for k in range(num_aeropuertos):
        for i in range(num_aeropuertos):
            for j in range(num_aeropuertos):
                distancias[i, j] = min(distancias[i, j], distancias[i, k] + distancias[k, j])
    
    return distancias

import heapq

def calcular_distancia_minima(aeropuerto_origen, aeropuerto_destino, df, distancias):
    grafo = {}
    for i, row in df.iterrows():
        aeropuerto = row['Nombre']
        grafo[aeropuerto] = []
        for j, neighbor_row in df.iterrows():
            if i != j:
                neighbor = neighbor_row['Nombre']
                distancia = distancias[i, j]
                grafo[aeropuerto].append((neighbor, distancia))

    # Algoritmo de Dijkstra con montículo binario
    distancias_dijkstra = {aeropuerto: math.inf for aeropuerto in grafo}
    distancias_dijkstra[aeropuerto_origen] = 0
    padres = {}

    # Utilizar el montículo binario para almacenar los aeropuertos con sus distancias
    heap = [(0, aeropuerto_origen)]

    while heap:
        distancia_actual, aeropuerto_actual = heapq.heappop(heap)

        if distancia_actual > distancias_dijkstra[aeropuerto_actual]:
            continue

        for vecino, distancia in grafo[aeropuerto_actual]:
            nueva_distancia = distancias_dijkstra[aeropuerto_actual] + distancia
            if nueva_distancia < distancias_dijkstra[vecino]:
                distancias_dijkstra[vecino] = nueva_distancia
                padres[vecino] = aeropuerto_actual
                heapq.heappush(heap, (nueva_distancia, vecino))

    distancia_minima = distancias_dijkstra[aeropuerto_destino]

    return distancia_minima

@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_excel('Aeropuertos.xlsx', sheet_name='Aeropuertos')
    aeropuertos = df['Nombre'].tolist()

    ruta_encontrada = None

    if request.method == 'POST':
        aeropuerto_origen = request.form['aeropuerto_origen']
        aeropuerto_destino = request.form['aeropuerto_destino']
        
        distancias = calcular_distancias_floyd_warshall(df)
        distancia_minima = calcular_distancia_minima(aeropuerto_origen, aeropuerto_destino, df, distancias)
        
        ruta_encontrada = f"La distancia más corta entre {aeropuerto_origen} y {aeropuerto_destino} es {distancia_minima} km."

        return ruta_encontrada

    return render_template('form.html', ruta_encontrada=ruta_encontrada, aeropuertos=aeropuertos)

