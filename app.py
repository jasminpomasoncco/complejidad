from flask import Flask, render_template, request
import pandas as pd
from geopy import distance
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def calcular_distancias_warshall(df):
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
    
    # Algoritmo de Warshall
    for k in range(num_aeropuertos):
        for i in range(num_aeropuertos):
            for j in range(num_aeropuertos):
                if distancias[i, j] > distancias[i, k] + distancias[k, j]:
                    distancias[i, j] = distancias[i, k] + distancias[k, j]
    
    # Ordenar la matriz de distancias como una matriz de adyacencia
    for i in range(num_aeropuertos):
        for j in range(num_aeropuertos):
            if distancias[i, j] == np.inf:
                distancias[i, j] = 0
    
    return distancias
    

def calcular_distancia_minima_dijkstra(aeropuerto_origen, aeropuerto_destino, df, distancias):
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

def calcular_ruta(aeropuerto_origen, aeropuerto_destino):
    # Your implementation for calculating the shortest route here
    # This can be any algorithm such as Dijkstra's algorithm or A* search
    
    # Return a placeholder route for now
    return [aeropuerto_origen, aeropuerto_destino]


@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_excel('Aeropuertos.xlsx', sheet_name='Aeropuertos')
    aeropuertos = df['Nombre'].tolist()

    ruta_encontrada = None
    graph_image = None

    if request.method == 'POST':
        aeropuerto_origen = request.form['aeropuerto_origen']
        aeropuerto_destino = request.form['aeropuerto_destino']
        
        distancias = calcular_distancias_warshall(df)
        distancia_minima = calcular_distancia_minima_dijkstra(aeropuerto_origen, aeropuerto_destino, df, distancias)

        # Calculate the shortest route using your implementation
        shortest_route = calcular_ruta(aeropuerto_origen, aeropuerto_destino)

        # Generate the graph image
        fig, ax = plt.subplots()
        im = ax.imshow(distancias, cmap='viridis')
        ax.set_xticks(np.arange(len(aeropuertos)))
        ax.set_yticks(np.arange(len(aeropuertos)))
        plt.setp(ax.get_xticklabels(), ha="right", rotation_mode="anchor")
        plt.colorbar(im, ax=ax, label='Distancia (km)')

        # Plot the shortest route
        route_indices = [aeropuertos.index(aeropuerto) for aeropuerto in shortest_route]
        ax.plot(route_indices, route_indices, 'r-', linewidth=2)

        plt.tight_layout()
        graph_image = 'graph.png'
        plt.savefig('static/' + graph_image)
        plt.close()

        ruta_encontrada = f"La distancia más corta entre {aeropuerto_origen} y {aeropuerto_destino} es {distancia_minima} km."

    return render_template('form.html', ruta_encontrada=ruta_encontrada, graph_image=graph_image, aeropuertos=aeropuertos)
