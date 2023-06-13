#IMPORTAR LIBRERÍAS A UTILIZAR PARA EL ANÁLISIS EXPLORATORIO DE DATOS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#IMPORTAR DATAFRAME QUE SURGIÓ DEL ANÁLISIS DE DATOS EXPLORATORIOS
data = pd.read_csv('dataset\df_stem.csv', sep=',', encoding="utf8")

#VECTORIZAR EL MODELO, REALIZAR LA MATRIZ DE ENTRENAMIENTO Y CAMBIO DE TIPO DE DATO, PARA 
#TRATA DE REDUCIR A LA MITAD EL PESO DEL MODELO.
tfidf =TfidfVectorizer()
data['tag_stem'] = data['tag_stem'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['tag_stem'].values) 
tfidf_matrix = tfidf_matrix.astype(np.float32)

#OBTENER EL MODELO PARA LLEVARLO A LA FUNCIÓN ENCARGADA DE HACER LAS RECOMENDACIONES
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)