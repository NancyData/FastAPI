#Importar librerías necesarias.
from fastapi import FastAPI
import pandas as pd
from modelo import cosine_sim, data

#Instanciar la clase con un título, una descripción.
app = FastAPI(title='PI_ML',
            description='Data 11')

#Primera función donde la API va a tomar mi dataframe para las consultas.
@app.get('/')
def index():
    return {"message": 'API realizada por Nancy Contreras'}

df_original = pd.read_csv('dataset\df_peliculas.csv', sep=",")
df = df_original.copy()

#CONSULTA NÚMERO 1: ingresas un mes en minúsculas y cómo respuesta obtienes la cantidad
#de películas estrenadas ese mes, en el histórico de datos
@app.get('/cantidad_filmaciones_mes/{mes}')
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
    return {'mes': mes,
            'cantidad': respuesta}

#CONSULTA NÚMERO 2: ingresas un día de la semana en minúsculas y cómo respuesta obtienes
#la cantidad de películas estrenadas ese mes, en el histórico de datos
@app.get('/cantidad_filmaciones_dia/{dia}')
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
    return {'dia': dia,
            'cantidad': respuesta}

#CONSULTA NÚMERO 3: ingresas un el título de una película y retorna el título, año estrenada
#la popularidad de la misma, por el contrario, si el dato no se encuentra en el histórico
#retorna un aviso.
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    fila = df[(df['title'] == titulo)].reset_index()
    if titulo in fila == False:
        return ("La película no fue escrita correctamente o no se encuentra dentro de la base de datos. Colocar la primera letra de cada palabra en mayúscula")
    else:
        titulo = titulo
        anio = fila.loc[0,'release_year']
        anio = int(anio)
        popularidad = fila.loc[0,'popularity']
        popularidad = int(popularidad)
        return {'titulo': titulo,
            'anio': anio,
            'popularidad': popularidad}
    
#CONSULTA NÚMERO 4: ingresas un el título de una película y retorna el título, año estrenada
#suma de votos y el promedio de la misma, por el contrario, si el dato no se encuentra en
#el histórico retorna un aviso.
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    fila = df[df['title'] == titulo].reset_index()
    if fila.empty:
        return ("La película no fue escrita correctamente o no se encuentra dentro de la base de datos. Colocar la primera letra de cada palabra en mayúscula")
    else:
        titulo = titulo
        anio = fila.loc[0, 'release_year']
        anio = int(anio)
        votos = fila.loc[0, 'vote_count']
        votos= int(votos)
        votos_prom = fila.loc[0,'vote_average']
        votos_prom= int(votos_prom)
        if votos < 2000:
            return 'La película {} no cumple con la cantidad mínima de valoraciones para obtener el promedio de votaciones'.format(titulo)
        else:
            return {'titulo': titulo,
            'anio': anio,
            'voto_total': votos, 
            'voto_promedio': votos_prom}

#CONSULTA NÚMERO 5: ingresas en nombre de un actor y retorna la cantidad de filmaciones
#que ha hecho, así cómo su éxito medido por la suma del retorni de sus películas, la suma
#de ellas y el promedio de retorno.
@app.get('/get_actor/{nombre}')
def get_actor(nombre:str):
    texto = df['cast'].astype(str)
    busqueda = texto.str.contains(nombre, case=False) 
    df_actor= df[busqueda].reset_index()
    if df_actor.empty:
        return ("El nombre del actor no fue escrito correctamente o no se encuentra dentro de la base de datos")
    else:
        peliculas = df_actor.shape[0]
        exito = df_actor['return'].sum() 
        retorno_promedio = df_actor['return'].mean() 
        return {'actor': nombre,
            'cantidad_filmaciones': peliculas,
            'retorno_total': exito, 
            'retorno_promedio': retorno_promedio}

#CONSULTA NÚMERO 6: ingresas en nombre de un director y retorna su éxito medido por la
#cantidad de películas que ha dirigido, la suma del retorno de ellas, y un listado de 
#las películas con el título, fecha de estreno, retorno individual, presupuesto y ganancia
@app.get('/get_director/{nombre}')
def get_director(nombre:str):
    texto = df['crew'].astype(str)
    busqueda = texto.str.contains(nombre, case=False) 
    df_director= df[busqueda].reset_index(drop=True)
    if df_director.empty:
        return ("El nombre del actor no fue escrito correctamente o no se encuentra dentro de la base de datos")
    else:
        peliculas = df_director.shape[0]
        peliculas = int(peliculas)
        exito = df_director['return'].sum() 
        exito = int(exito)
        df_peliculas = df_director[['title', 'release_date', 'return', 'budget', 'revenue']].reset_index(drop=True)
        df_peliculas = df_peliculas.to_dict()
        return {'director': nombre,
                     'retorno_total_director': exito,
                     'peliculas': peliculas,
                     'peliculas_data': df_peliculas}
  
#CONSULTA NÚMERO 7: al ingresar una película, retornará una recomendación de 5 películas
#de acuerdo con la ingresada previamente.
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
  idx = data[data['title']==titulo].index[0]
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
  sim_scores = sim_scores[1:6]
  movie_indices = [i[0] for i in sim_scores]
  pelis =  data['title'].iloc[movie_indices]
  return {'lista recomendada': pelis}