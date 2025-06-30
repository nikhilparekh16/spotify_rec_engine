# Spotify Music Recommendation Engine

This project is an interactive web application that recommends similar songs based on user input using NLP and the Spotify Web API.

##  Features

- **Search and Recommend Songs**: Type a song + artist to get 5 recommendations with cover art.
-  **NLP-powered Matching**: Uses TF-IDF vectorization and cosine similarity for lyric-based recommendation.
-  **Spotify API Integration**: Fetches real-time song metadata and cover art via Spotify Web API.
-  **Dataset Processing**: Filters and preprocesses a 1M+ track dataset using NLTK.

##  Technologies Used

- Python
- Streamlit
- Scikit-learn
- NLTK
- Spotipy
- Pandas
- Spotify Web API

##  How It Works

1. Preprocess lyrics using NLTK tokenization and stemming.
2. Vectorize lyrics using `TfidfVectorizer`.
3. Compute pairwise cosine similarity between all songs.
4. When a user selects a song, fetch the top similar songs from the matrix.
5. Use Spotify API to show cover art for recommended songs.

##  Run It Locally

1. **Clone the repo**:
   ```bash
   git clone https://github.com/nikhilparekh16/spotify_rec_engine.git
   cd spotify_rec_engine
