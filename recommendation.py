import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Load datasets
movies = pd.read_csv("D:/INTERNSHIP/movie recommendation/movies.csv")
ratings = pd.read_csv("D:/INTERNSHIP/movie recommendation/ratings.csv")

# Clean genres column
movies['genres'] = movies['genres'].fillna('').str.replace('|', ' ').str.lower()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

def get_all_movie_titles():
    return movies['title'].tolist()

def get_content_recommendations(title, top_n=5):
    if title not in indices:
        return ["Movie not found in dataset."]
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()

user_movie_matrix = ratings.merge(movies, on='movieId')
pivot = user_movie_matrix.pivot_table(index='userId', columns='title', values='rating').fillna(0)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(pivot.T.values)

def get_collaborative_recommendations(title, top_n=5):
    if title not in pivot.columns:
        return ["Movie not rated by enough users."]
    query_index = list(pivot.columns).index(title)
    distances, indices_knn = model_knn.kneighbors([pivot.T.values[query_index]], n_neighbors=top_n+1)
    recs = [pivot.columns[i] for i in indices_knn.flatten()]
    return recs[1:]


def get_all_genres():
    genre_set = set()
    for genre_str in movies['genres']:
        genre_set.update(genre_str.split())
    common_genres = {'romance', 'horror', 'sci-fi', 'crime', 'fantasy', 'thriller', 'action', 'comedy', 'drama'}
    available_genres = [genre for genre in common_genres if genre in genre_set]
    return sorted(available_genres)

def get_movies_by_genre(genre_name):
    genre_name = genre_name.lower()
    matched = movies[movies['genres'].str.contains(genre_name, case=False, na=False)]
    return matched['title'].tolist()
