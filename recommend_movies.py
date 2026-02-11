import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
import os

# Carregar modelo BERT pré-treinado
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_movie_embedding(title, overview, genres):
    # Gera embedding usando BERT
    text = f"title: {title}. overview: {overview}. genres: {genres}"
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

def recommend_movies(input_embedding, movies, top_n=5):
    # Calcular similaridade de cosseno entre o input e os embeddings dos filmes
    similarities = cosine_similarity([input_embedding], movie_embeddings)[0]

    # Criar uma cópia do DataFrame original para não modificar os dados originais
    movies_copy = movies.copy()

    # Adicionar similaridades ao DataFrame
    movies_copy['similarity'] = similarities

    # Excluir filmes sem overview
    movies_copy = movies_copy[movies_copy['overview'].str.strip() != ""]

    # Excluir filmes sem gender
    movies_copy = movies_copy[movies_copy['genres'].str.strip() != ""]

    # Ordenar pelos mais similares e retornar os top_n
    recommended = movies_copy.sort_values(by='similarity', ascending=False).head(top_n)

    return recommended[['title', 'overview', 'similarity']]

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "movies_with_embeddings.pkl")

movies = pd.read_pickle(path)
movie_embeddings = list(movies['embedding'])

# Input do usuário
#input_description = input("Enter a movie description: ")
#input_embedding = get_movie_embedding(input_description, input_description, input_description)

# Obter recomendações
#recommended_movies = recommend_movies(input_embedding, movies, top_n=5)

#print(recommended_movies)