import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
#from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
#import torch
import os

# Carregar modelo BERT pré-treinado
#tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#model = BertModel.from_pretrained('bert-base-uncased')

# Carregar modelo SentenceTransformer pré-treinado
model = SentenceTransformer('all-mpnet-base-v2')

def get_embedding(text: str):
    embedding = model.encode(text)
    return embedding

def get_overall_similarities(sim_title, sim_overview, sim_genres):
    #sim = (sim_title + sim_overview + sim_genres) / 3
    #sim = np.maximum(np.maximum(sim_title, sim_overview), sim_genres)
    sim = 0.35 * sim_title + 0.5 * sim_overview + 0.15 * sim_genres
    return sim

def recommend_movies(input_embedding, movies: pd.DataFrame, style: str, top_n=5):

    if style == 'combined_texts':
        
        # Similaridade com embedding combinado
        similarities = cosine_similarity([input_embedding], movies['embedding'])[0]

    elif style == 'title_overview_genres':
        
        # Similaridades separadas
        title_sim = cosine_similarity(
            [input_embedding], 
            np.vstack(movies['embedding_title'])
        )[0]

        overview_sim = cosine_similarity(
            [input_embedding], 
            np.vstack(movies['embedding_overview'])
        )[0]

        genres_sim = cosine_similarity(
            [input_embedding], 
            np.vstack(movies['embedding_genres'])
        )[0]

        # Média das similaridades
        similarities = get_overall_similarities(title_sim, overview_sim, genres_sim)
        
    movies_copy = movies.copy()
    movies_copy['similarity'] = similarities

    # Excluir filmes sem overview
    movies_copy = movies_copy[movies_copy['overview'].str.strip() != ""]

    # Excluir filmes sem genres
    movies_copy = movies_copy[movies_copy['genres'].str.strip() != ""]

    recommended = movies_copy.sort_values(
        by='similarity', ascending=False
    ).head(top_n)

    return recommended[['title', 'overview', 'similarity']]

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "movies_with_embeddings_all-mpnet-base-v2.pkl")

movies = pd.read_pickle(path)

# Input do usuário
#input_description = input("Enter a movie description: ")
#input_embedding = model.encode(input_description)

# Obter recomendações
#recommended_movies = recommend_movies(input_embedding, movies, top_n=5)

#print(recommended_movies)