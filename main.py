#Importar librerías necesarias.
from fastapi import FastAPI
import pandas as pd
import datetime

#Instanciar la clase con un título, una descripción.
app = FastAPI(title='PI_ML',
            description='Data 11')

#Primera función donde la API va a tomar mi dataframe para las consultas.
@app.get('/')
def index():
    return {"message": 'API realizada por Nancy Contreras'}

df_original = pd.read_csv('dataset\df_peliculas.csv', sep=",")
df = df_original.copy()

#CORRECTA
@app.get('/cantidad_filmaciones_mes/')
def cantidad_filmaciones_mes(mes:str):
     #Defino los meses:
    if mes == "enero":
        mes_ing = 1
    elif mes == "febrero":
        mes_ing = 2
    elif mes == "marzo":
        mes_ing = 3
    elif mes == "abril":
        mes_ing = 4
    elif mes == "mayo":
        mes_ing = 5
    elif mes == "junio":
        mes_ing = 6
    elif mes == "julio":
        mes_ing = 7
    elif mes == "agosto":
        mes_ing = 8
    elif mes == "septiembre":
        mes_ing = 9
    elif mes == "octubre":
        mes_ing = 10
    elif mes == "noviembre":
        mes_ing = 11
    elif mes == "diciembre":
        mes_ing = 12
    else:
        return ("Mes ingresado incorectamente. Favor ingresar mes en español, en minúsculas y sin abreviatura")
    df_mes= df[df['release_date'].apply(pd.to_datetime).dt.month == mes_ing]
    respuesta = df_mes.shape[0]
    return 'En total {} películas fueron estrenadas en el mes de {} en todo el histórico'.format(respuesta, mes)

#CORRECTA
@app.get('/cantidad_filmaciones_dia/')
def cantidad_filmaciones_dia(dia:str):
    #Defino los días de la semana:
    if dia == "lunes":
        dia_ing = 1
    elif dia == "martes":
        dia_ing = 2
    elif dia == "miercoles":
        dia_ing = 3
    elif dia == "jueves":
        dia_ing = 4
    elif dia == "viernes":
        dia_ing = 5
    elif dia == "sabado":
        dia_ing = 6
    elif dia == "domingo":
        dia_ing = 7
    else:
        return ("Día ingresado incorectamente. Favor ingresar día en español, en minúsculas, sin abreviatura y sin acento")
    df_mes= df[df['release_date'].apply(pd.to_datetime).dt.weekday == dia_ing]
    respuesta = df_mes.shape[0]
    return 'En total {} películas fueron estrenadas los días {} de todo el histórico'.format(respuesta, dia)
    return

#CORRECTA
@app.get('/score_titulo/')
def score_titulo(titulo:str):
    fila = df[(df['title'] == titulo)].reset_index()
    if titulo in fila == False:
        return ("La película no fue escrita correctamente o no se encuentra dentro de la base de datos")
    else:
        titulo = titulo
        anio = fila.loc[0,'release_year']
        popularidad = fila.loc[0,'popularity']
        return 'La película {} fue estrenada en el año {} alcanzando una popularidad de {}'.format(titulo, anio, popularidad)
    
#CORRECTA
@app.get('/votos_titulo/')
def votos_titulo(titulo:str):
    fila = df[df['title'] == titulo].reset_index()
    if fila.empty:
        return ("La película no fue escrita correctamente o no se encuentra dentro de la base de datos")
    else:
        titulo = titulo
        anio = fila.loc[0, 'release_year']
        votos = fila.loc[0, 'vote_count']
        votos_prom = fila.loc[0,'vote_average']
        if votos < 2000:
            return 'La película {} no cumple con la cantidad mínima de valoraciones para obtener el promedio de votaciones'.format(titulo)
        else:
            return 'La película {} estrenada en el año {} cuenta con {} votaciones y una calificación promedio de {}'.format(titulo, anio, votos, votos_prom)

#CORRECTA
@app.get('/get_actor/')
def get_actor(nombre:str):
    texto = df['cast'].astype(str)
    busqueda = texto.str.contains(nombre, case=False) 
    df_actor= df[busqueda].reset_index()
    if df_actor.empty:
        return ("El nombre del actor no fue escrito correctamente o no se encuentra dentro de la base de datos")
    else:
        peliculas = df_actor.shape[0]
        exito = df_actor['return'].mean() 
        return ('El actor {} ha participado en {} filmaciones y ha conseguido un retorno promedio de {:.2F} por filmación'.format(nombre, peliculas, exito))

#CORRECTA
@app.get('/get_director/')
def get_director(nombre:str):
    texto = df['crew'].astype(str)
    busqueda = texto.str.contains(nombre, case=False) 
    df_director= df[busqueda].reset_index(drop=True)
    if df_director.empty:
        return ("El nombre del actor no fue escrito correctamente o no se encuentra dentro de la base de datos")
    else:
        peliculas = df_director.shape[0]
        exito = df_director['revenue'].mean() 
        df_peliculas = df_director[['title', 'release_date', 'return', 'budget', 'revenue']]
        return (f'{nombre} ha dirigido {peliculas} filmaciones, alcanzando unos ingresos promedio de {exito:.2F} por filmación. Dichas películas son:\n{df_peliculas.to_string}')