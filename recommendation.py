''' Nuestro modelo de recomendacion lo realice en un .py ya que voy a tener que exportar la variable
    del coseno de similiritud ya que es muy pesada y nos conviene correrla una sola vez
'''

import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer # Importamos nuestro CountVectorizer de sklearn
from sklearn.metrics.pairwise import cosine_similarity # Y nuestro coseno de simil
df_games = pd.read_parquet('clean_games.parquet.gzip') # Leemos nuestros juegos
games = df_games.sample(frac=0.1, random_state=42) #Reducimos el dataset por un problema de rendimiento

generos_a_excluir = [ # Creamos una lista de los generos menos vistos en el dataset, esto lo hacemos para reducir el tamaño
                      # del dataset por motivos de rendimiento, aunque por el otro lado perdemos precision en nuestro modelo
 'Simulation',
 'Strategy',
 'Free to Play',
 'RPG',
 'Sports',
 '[]',
 'Racing',
 'Early Access',
 'Massively Multiplayer',
 'Animation &amp; Modeling',
 'Video Production',
 'Utilities',
 'Web Publishing',
 'Education',
 'Software Training',
 'Design &amp; Illustration',
 'Audio Production',
 'Photo Editing',
 'Accounting']

for i in generos_a_excluir:
    games = games[games['genres'] != i] # Eliminamos los juegos que sean de esos generos


games.dropna(inplace=True) # Eliminamos valores faltantes
co = CountVectorizer(max_features=7000, stop_words='english') # Creamos nuestro contador de vectores con un maximo de 7000 regs
                                                              # Tambien aprovechamos y por las dudas, eliminamos nuestras stopwords
vector = co.fit_transform(games['genres']).toarray() # Creamos nuestro vector, entrenandolo con nuestra principal variable predictora, generos
co.get_feature_names_out() # Extraemos los nombres de los features
cosine_sim = cosine_similarity(vector) # Y creamos nuestro coseno, cabe aclarar que hubo mucho tiempo de pruebas, ya que esta linea
                                       # No funciona con el dataset completo, ni en mi pc ni en Colab, reducido de 70mil x 70mil
                                       # a 30mil x 30mil si corre aunque demore.
