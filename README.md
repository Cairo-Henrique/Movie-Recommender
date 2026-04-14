# Movie Recommender

This project is a content-based movie recommendation system that utilizes Natural Language Processing to suggest films based on the semantic meaning of user descriptions. Unlike keyword-based search engines, this system employs deep learning embeddings to understand the context and themes provided in a text prompt.

![Screenshot of the site as seen by the user](assets/site_screenshot.png)

## Project Overview

The core of the application relies on converting movie metadata into high-dimensional vectors. By calculating the Cosine Similarity between a user's input and a pre-processed database of films, the engine identifies movies with the highest thematic relevance. The system is designed with a Flask backend and a modern, responsive web interface.

## Dataset

The project utilizes the **TMDB 10,000 Movies Dataset (Updated 2022)**. This dataset provides comprehensive metadata for approximately 10,000 films, including the specific fields required for both the recommendation logic and the user interface.

## Methodology

The recommendation logic is divided into two primary phases:

### 1. Vectorization and Data Processing
The data pipeline, documented in `movies_embeddings_creation.ipynb`, processes the metadata through the following steps:
* **Model Selection**: Uses the `all-mpnet-base-v2` model from the Sentence Transformers library to generate embeddings.
* **Feature Extraction**: Cleans and treats metadata columns for titles, overviews, and genres.
* **Granular Embedding Generation**: Creates separate vectors for the title, overview, and genres of each film to allow for specific weighting.

### 2. Recommendation Logic
The engine utilizes a weighted linear combination to determine the final similarity score:
* **Weight Distribution**: The system assigns $0.5$ to the overview, $0.35$ to the title, and $0.15$ to the genres.
* **Similarity Calculation**: Employs Scikit-Learn’s `cosine_similarity` to compare the input embedding against the stored vectors.
* **Filtering**: Automatically excludes entries with empty overviews or missing genre tags to ensure recommendation quality.

## Technical Stack

* **Backend**: Python, Flask
* **Data Science**: Pandas, NumPy, Scikit-Learn, Sentence-Transformers, PyTorch
* **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript

## Installation and Setup

### Prerequisites
* Python 3.8 or higher
* Pip package manager

### Local Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Cairo-Henrique/Movie-Recommender.git
   cd Movie-Recommender
   ```
2. Install the required dependencies
3. Generate the embedding database (if not present):
   * Open `movies_embeddings_creation.ipynb` and execute the cells to generate the `.pkl` file containing the vectors.
4. Launch the application:
   ```bash
   python app.py
   ```

## Repository Structure

* `app.py`: The main Flask application handling routing and recommendation requests.
* `app_functions.py`: The code for the `movies` dataset and the main functions used in `app.py`.
* `movies_embeddings_creation.ipynb`: The research and development notebook used for data cleaning and embedding generation.
* `static/`: Contains the CSS for the glassmorphism interface and JavaScript for interactive UI elements.
* `templates/`: HTML templates for the web interface.
* `movies.csv`: original IMDB movies dataset.
* `dataset_treatment.py`: data cleaning of the original movies dataset; output: `movies_fixed.py`.
* `movies_fixed.csv`: The treated dataset containing movie metadata.
