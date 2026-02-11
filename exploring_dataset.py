import pandas as pd
import os
from pathlib import Path

# Caminho absoluto da pasta onde o script está
base_dir = Path(os.path.dirname(os.path.abspath(__file__)))

# Caminho absoluto do arquivo CSV corrigido
movies_path = base_dir / 'movies_fixed.csv'

# Leitura do arquivo
movies = pd.read_csv(movies_path, encoding='utf-8')

def analyze_movies(df):
    print("Analisando dataset de filmes...")
    print(f"Número de linhas: {len(df)}")
    print(f"Número de colunas: {len(df.columns)}")
    print("Colunas disponíveis:", df.columns.tolist())
    
    # Exemplo de análise: contar filmes por ano
    if 'year' in df.columns:
        year_counts = df['year'].value_counts().sort_index()
        print("Número de filmes por ano:")
        print(year_counts)
    
    # Exemplo de análise: filmes por gênero
    if 'genres' in df.columns:
        genre_counts = df['genres'].value_counts()
        print("Número de filmes por gênero:")
        print(genre_counts)

def show_movies_of_year(df, year):
    if 'year' in df.columns:
        filtered = df[df['year'] == year]
        print(f"Filmes do ano {year}:")
        filtered = filtered['title']
        print(filtered.to_string(index=False))
    else:
        print("Coluna 'year' não encontrada no dataset.")

def show_summary_of(df, title):
    filtered = df[df['title'].str.lower() == title.lower()]
    if not filtered.empty:
        overview = filtered.iloc[0]['overview']
        return overview
    else:
        return False

analyze_movies(movies)

#show_movies_of_year(movies, 0)

print(show_summary_of(movies, 'Jurassic Park'))