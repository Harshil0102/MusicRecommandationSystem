from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import random
import pandas as pd
from scipy.sparse import csr_matrix

app = Flask(__name__, static_folder='Content')

client_credentials_manager = SpotifyClientCredentials(client_id='380a6b3535dc420a905dccf328a0e165', client_secret='b0ca7947448246d28aafc40f49610cf4')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to search for a song on Spotify by its title and artist name
def search_song_on_spotify(query):
    try:
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'spotify_id': track['id'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            }
        else:
            return None
    except Exception as e:
        print(f"Error searching for song: {e}")
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('Index.html')

@app.route('/search', methods=['GET'])
def searchonspotify():
    return render_template('SongList.html')
    
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    search_result = search_song_on_spotify(query)
    return jsonify(search_result)

if __name__ == '__main__':
    app.run(debug=True)
