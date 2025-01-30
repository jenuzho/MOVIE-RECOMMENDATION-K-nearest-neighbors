from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Cargar el modelo KNN y el DataFrame
# Suponiendo que los archivos 'knn_model.pkl' y 'movies_df.pkl' están en la misma carpeta
knn_model = pickle.load(open('knn_model.pkl', 'rb'))
df = pd.read_csv("base_movies.csv")


vect = TfidfVectorizer(token_pattern=r'\b\w+\b', lowercase=True)
matrix = vect.fit_transform(df['tags'])

app = Flask(__name__)

# Función para obtener recomendaciones
def get_movie_recommendations(movie_title):
    movie_index = df[df["title"] == movie_title].index[0]
    distances, indices = knn_model.kneighbors(matrix[movie_index])
    # Guardamos la distancia, pero la excluimos del output
    similar_movies = [(df["title"][i], distances[0][j]) for j, i in enumerate(indices[0])]
    return similar_movies[1:]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie']  # Obtenemos el título de la película desde el formulario
    recommendations = get_movie_recommendations(movie_title)
    return render_template('index.html', recommendations=recommendations, selected_movie=movie_title)

if __name__ == '__main__':
    app.run(debug=True)
