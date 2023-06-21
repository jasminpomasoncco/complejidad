from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    df = pd.read_excel('Aeropuertos.xlsx', sheet_name='Aeropuertos')
    
    aeropuertos = df['Nombre'].tolist()
    
    return render_template('form.html', ruta_encontrada=None, aeropuertos=aeropuertos)


