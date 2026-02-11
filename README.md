# Movie-Recommender

A Movie Recommender system built with Python that generates movie recommendations using embedding representations and similarity search.

This project implements an end-to-end pipeline including data preprocessing, embedding generation, similarity computation, and a web interface for serving recommendations.

---

## Methodology

### Data Processing

- Cleaned and standardized movie metadata
- Processed categorical features such as genres
- Generated a structured dataset (`movies_fixed.csv`) for modeling

### Movie Embeddings

- Converted movie features into numerical vector representations
- Trained embeddings using Python-based preprocessing
- Stored embeddings for efficient similarity computation

### Recommendation Engine

- Implemented cosine similarity for movie comparison
- Used nearest-neighbor retrieval to generate recommendations
- Returned top-N most similar movies for a selected input

### Web Application

- Implemented with a Flask-style Python structure
- `app.py` serves recommendation results
- `templates/` and `static/` provide the user interface

---

## Tech Stack

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- Jupyter Notebook  
- Flask  
- HTML / CSS  

