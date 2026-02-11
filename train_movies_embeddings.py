import pandas as pd
import os
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch

# Caminho absoluto do arquivo CSV corrigido no ambiente Colab
movies_path = '/content/movies_fixed.csv' # Updated path

# Leitura do arquivo
movies = pd.read_csv(movies_path, encoding='utf-8')

# Carregar modelo BERT pré-treinado
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_movie_embedding(overview):
    # Gera embedding usando BERT
    inputs = tokenizer(overview, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# Preencher valores nulos na coluna 'overview' com ''
movies['overview'] = movies['overview'].fillna('').astype(str)

# Gerar embeddings para todos os filmes
movies['embedding'] = movies['overview'].apply(get_movie_embedding)
movie_embeddings = list(movies['embedding'])

# Input do usuário
input_description = input("Enter a movie description: ")
input_embedding = get_movie_embedding(input_description)

def recommend_movies(input_embedding, movies, top_n=5):
    # Calcular similaridade de cosseno entre o input e os embeddings dos filmes
    similarities = cosine_similarity([input_embedding], movie_embeddings)[0]

    # Criar uma cópia do DataFrame original para não modificar os dados originais
    movies_copy = movies.copy()

    # Adicionar similaridades ao DataFrame
    movies_copy['similarity'] = similarities

    # Ordenar pelos mais similares e retornar os top_n
    recommended = movies_copy.sort_values(by='similarity', ascending=False).head(top_n)

    return recommended[['title', 'overview', 'similarity']]

# Obter recomendações
recommended_movies = recommend_movies(input_embedding, movies, top_n=5)

print("Recommended Movies:")
print(recommended_movies)
