import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

movie = pd.read_csv('/workspaces/Projeto_IA/BD/TMDB_tv_dataset_v3.csv')

movie['genres'] = movie['genres'].str.split(', ')

def recommend_movies_by_genre(input_genre, min_popularity=5000,num_recommendations=5, exclude_adult=True):
    # Filtrar filmes que têm o gênero de entrada
    filtered_movies = movie[movie['genres'].apply(lambda x: input_genre in x if isinstance(x, list) else False)]

    if exclude_adult:
        # Excluir filmes para maiores de 18 anos
        filtered_movies = filtered_movies[filtered_movies['adult'] == False]

    if filtered_movies.empty:
        print(f"Nenhum filme encontrado no gênero '{input_genre}'")
        return

    # Ordenar os filmes por alguma métrica (por exemplo, popularidade ou classificação) e obter os 5 melhores
    recommended_movies = filtered_movies.sort_values(by='popularity', ascending=False).head(num_recommendations)

    return recommended_movies

# Teste o sistema de recomendação com um gênero de filme de entrada
input_genre = 'Action'  # Substitua pelo gênero de interesse
recommendations = recommend_movies_by_genre(input_genre)

if recommendations is not None:
    print(f"Recomendações de filmes no gênero '{input_genre}':")
    print(recommendations[['name', 'popularity', 'adult']])