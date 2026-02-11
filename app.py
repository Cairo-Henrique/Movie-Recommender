from flask import Flask, render_template, request
from recommend_movies import get_movie_embedding, recommend_movies, movies
import os
import pandas as pd

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # pega o texto que o usuário digitou no input do HTML
        input_description = request.form['description']

        # gera embedding e recomendações
        input_embedding = get_movie_embedding(input_description,
                                              input_description,
                                              input_description)
        recommended_movies = recommend_movies(input_embedding, movies, top_n=5)

        # transforma em lista para passar ao HTML
        output = []
        for index, row in recommended_movies.iterrows():
            output.append((row['title'], row['overview']))
        
        return render_template('index.html', results=output)

    # caso seja GET, mostra apenas a página vazia
    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)