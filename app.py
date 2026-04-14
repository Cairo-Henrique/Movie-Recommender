from flask import Flask, render_template, request
from Movies.functions import get_embedding, recommend_movies, movies

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # pega o texto que o usuário digitou no input do HTML
        input_description = request.form['description'].strip()
        
        # se o input estiver vazio, mostra a página sem resultados
        if input_description == '':
            return render_template('index.html', results=None)

        # pega o número de filmes que o usuário seleicionou no dropdown do HTML
        top_n = int(request.form['top_n'])

        # gera embedding e recomendações
        input_embedding = get_embedding(input_description)
        recommended_movies = recommend_movies(input_embedding, movies, style='title_overview_genres', top_n=top_n)

        # transforma em lista para passar ao HTML
        output = []
        for index, row in recommended_movies.iterrows():
            output.append((row['title'], row['overview']))
        
        return render_template('index.html', results=output)

    # caso seja GET, mostra apenas a página vazia
    return render_template('index.html', results=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
