import pickle
import streamlit
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# initialize spotify client
client_credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)

def get_song_coverart_url(song_name, artist_name):
    search = f"track:{song_name} artist:{artist_name}"
    result = sp.search(q=search, type="track")

    if result and result["tracks"]["items"]:
        track = result["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(song):
    index = dataframe[dataframe['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_artists = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = dataframe.iloc[i[0]].artist
        print(artist)
        print(dataframe.iloc[i[0]].song)
        recommended_music_posters.append(get_song_coverart_url(dataframe.iloc[i[0]].song, artist))
        recommended_music_names.append(dataframe.iloc[i[0]].song)
        recommended_music_artists.append(dataframe.iloc[i[0]].artist)

    return recommended_music_names,recommended_music_posters, recommended_music_artists


streamlit.header('Spotify Song Recommender')
dataframe = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = dataframe['song'].values
artist_list = dataframe['artist'].values
dataframe['song,artist'] = dataframe['song'] + ',\t' + dataframe['artist']
song_artist = dataframe['song,artist'].values
selected_song_artist = streamlit.selectbox(
    "Type or Pick a Song/Artist",
    song_artist
)
selected_song = selected_song_artist.split(',\t')[0]

if streamlit.button('Show Recommendations'):
    recommended_music_names,recommended_music_posters, recommended_music_artists = recommend(selected_song)
    col1, col2, col3, col4, col5= streamlit.columns(5)
    with col1:
        streamlit.text(recommended_music_names[0])
        streamlit.text(recommended_music_artists[0])
        streamlit.image(recommended_music_posters[0])
    with col2:
        streamlit.text(recommended_music_names[1])
        streamlit.text(recommended_music_artists[1])
        streamlit.image(recommended_music_posters[1])

    with col3:
        streamlit.text(recommended_music_names[2])
        streamlit.text(recommended_music_artists[2])
        streamlit.image(recommended_music_posters[2])
    with col4:
        streamlit.text(recommended_music_names[3])
        streamlit.text(recommended_music_artists[3])
        streamlit.image(recommended_music_posters[3])
    with col5:
        streamlit.text(recommended_music_names[4])
        streamlit.text(recommended_music_artists[4])
        streamlit.image(recommended_music_posters[4])