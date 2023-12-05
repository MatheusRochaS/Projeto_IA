##Dataset url: https://grouplens.org/datasets/movielens/latest/

import pandas as pd
import numpy as np

pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

movies_df = pd.read_csv('https://raw.githubusercontent.com/mfmarlonferrari/KNN_recommender/main/movies.csv',usecols=['movieId','title'],dtype={'movieId': 'int32', 'title': 'str'})

series_df = pd.read_csv('https://raw.githubusercontent.com/MatheusRochaS/Projeto_IA/main/BD/test.csv?token=GHSAT0AAAAAACKY4VWMCGAMHMGMXBSELEY6ZLPU2IQ',usecols=['id','original_name'],dtype={'id': 'int32', 'original_name': 'str'})
series_df

movies_df.head()

rating_df=pd.read_csv('https://raw.githubusercontent.com/mfmarlonferrari/KNN_recommender/main/ratings.csv',usecols=['userId', 'movieId', 'rating'],
    dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})

rating_df.head()

df = pd.merge(rating_df,movies_df,on='movieId')
df.head()

df.shape

movie_features_df=df.pivot_table(index='userId',columns='title',values='rating').fillna(0)
movie_features_df.head()

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df)

movie_features_df.shape

query_index = 444
distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1,-1), n_neighbors = 4)

usuario = movie_features_df.index[query_index]

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recomendando para usuário {0}:\n'.format(usuario))
    else:
        print('Usuário recomendado {0}: {1}, distância de {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))

idx_recomendado = movie_features_df.index[indices.flatten()[1]]

idx_recomendado

recomendado = movie_features_df.loc[idx_recomendado].to_frame()
base = movie_features_df.loc[usuario].to_frame()

#PEGA OS FILMES QUE O USUARIO AINDA NAO ASSISTIU
novos_titulos = pd.merge(base,recomendado,on='title',how='inner').sort_values(by=idx_recomendado, ascending=False)
novos_titulos = novos_titulos[(novos_titulos[idx_recomendado] > 0) & (novos_titulos[usuario] == 0)].reset_index()
novos_titulos

novos_titulos.title