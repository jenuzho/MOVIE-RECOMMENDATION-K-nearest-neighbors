from flask import Flask, render_template, request
import pandas as pd

# Inicializar Flask
app = Flask(__name__)

# Cargar el dataset
movies = pd.read_csv("src/base_movies.csv")

# Ruta de inicio
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para procesar recomendaciones por género
@app.route("/recommend_by_genre", methods=["POST"])
def recommend_by_genre():
    # Obtener el género seleccionado por el usuario
    selected_genre = request.form.get("genre")

    # Filtrar películas por género
    filtered_movies = movies[movies["genres"].str.contains(selected_genre, na=False)]

    # Obtener los títulos de las primeras 10 películas del género
    recommendations = filtered_movies.head(10)[["title", "poster_path"]].to_dict(orient="records")

    # Renderizar la página con las recomendaciones
    return render_template("index.html", recommendations=recommendations)

# Ejecutar la aplicación localmente
if __name__ == "__main__":
    app.run(debug=True)
