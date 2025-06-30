import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Download NLTK tokenizer once
nltk.download('punkt_tab')

def load_and_clean_data(csv_path):
    print("Loading data...")
    df = pd.read_csv(csv_path)

    artists_to_drop = [
        'ABBA', 'Warren Zevon', 'Ace Of Base', 'Adam Sandler', 'Little Mix',
        'Neil Young', 'Beautiful South', 'Wishbone Ash', 'Counting Crows',
        'Peter Cetera', 'Aerosmith', 'Air Supply', 'Aiza Seguerra',
        'Alabama', 'Alan Parsons Project'
    ]
    df = df.drop(df[df['artist'].isin(artists_to_drop)].index)

    df = df.sample(7000).drop('link', axis=1).reset_index(drop=True)

    # Lowercase + clean text
    df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex=True)

    # Tokenize + stem
    stemmer = PorterStemmer()
    def tokenizer(txt):
        tokens = nltk.tokenize.word_tokenize(txt)
        stemming = [stemmer.stem(t) for t in tokens]
        return " ".join(stemming)
    
    print("Tokenizing and stemming...")
    df['text'] = df['text'].apply(tokenizer)

    return df

def compute_similarity(df):
    tfidvector = TfidfVectorizer(analyzer='word', stop_words='english')
    matrix = tfidvector.fit_transform(df['text'])
    similarity = cosine_similarity(matrix)
    return similarity

def recommendation(song_df, df, similarity):
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    song_list = [df.iloc[m_id[0]].song for m_id in distances[1:21]]
    return song_list

if __name__ == "__main__":
    # Check if we already have the pickle files
    if os.path.exists("df.pkl") and os.path.exists("similarity.pkl"):
        print("Loading existing data...")
        df = pickle.load(open('df.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
    else:
        df = load_and_clean_data("spotify_millsongdata.csv")
        similarity = compute_similarity(df)

        # Save results
        pickle.dump(df, open('df.pkl', 'wb'))
        pickle.dump(similarity, open('similarity.pkl', 'wb'))
        print("Data processed and saved to pickle files.")

    # Example: show recommendations for a song
    try:
        recs = recommendation('Bang', df, similarity)
        print(f"Recommendations for 'Bang': {recs}")
    except IndexError:
        print("Song not found in dataset!")
