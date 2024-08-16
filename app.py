from flask import Flask, render_template, request, jsonify, render_template, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import random
import pandas as pd
from scipy.sparse import csr_matrix
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import joblib
import random
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
from spotipy.oauth2 import SpotifyClientCredentials
import os
from PIL import Image


app = Flask(__name__, static_folder='Content')
mail="h1@gmail.com"


#Harjot Changes
app.secret_key = "2dcf15dcc7d5ec9958ceb1c2a6bc249e9b774f5538ae83e6"  # Set your secret key here

# Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("credentials").sheet1
spreadsheet = client.open("credentials")
sheet_fav = spreadsheet.get_worksheet(1)

# Access the worksheet by index (0-based index)
sheet_fav = spreadsheet.get_worksheet(1)

client_credentials_manager = SpotifyClientCredentials(client_id='380a6b3535dc420a905dccf328a0e165', client_secret='b0ca7947448246d28aafc40f49610cf4')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_users_from_sheet():
    records = sheet.get_all_records()
    return {record['mail']: record['password'] for record in records}

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

@app.route('/')
def home():
        print("first")
        return render_template('login.html') 

@app.route('/login', methods=['POST'])
def login():
    print("second")
    if request.method == 'POST':
        mail = request.form['mail'].lower()
        password = request.form['password']
        print(f"Received mail: {mail}, password: {password}")
        users = get_users_from_sheet()
        print(f"Users from sheet: {users}")
        if mail in users:
            stored_password = str(users.get(mail)).strip() 
            print(f"Stored password for '{mail}': '{stored_password}'")
            if stored_password == password:
                print(f"Password matches for mail: {mail}")
                session['mail'] = mail
                return redirect(url_for('landing'))
            else:
                print(f"Password does not match for mail: {mail}")
                return render_template('login.html', error='Password does not match for mail')
        else:
            print(f"mail {mail} not found in users")
            return render_template('login.html', error='User not found')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        mail = request.form['mail'].lower() 
        password = request.form['password']
        retype_password = request.form['retype_password']

        # Check if passwords match
        if password != retype_password:
            return render_template('first-time-user.html', error='Passwords do not match')

        # Check if email already exists
        users = get_users_from_sheet()
        if mail in users:
            return render_template('first-time-user.html', error='Email already exists')

        add_user_to_sheet(mail, password)

        # Set session and redirect
        session['mail'] = mail
        return redirect(url_for('landing'))

    return render_template('first-time-user.html')

def favourites(mail, song_title, url, feed):
    # url = URL
    sheet_fav.append_row([mail, song_title, url, feed])

def getfavourites(mail):
    # Retrieve all records from the Google Sheet
    likedsongs = sheet_fav.get_all_records()

    liked_songs_list = []

    normalized_mail = mail.lower().strip()

    for record in likedsongs:
        # Normalize the mail in the record for comparison
        record_mail = record.get('mail', '').lower().strip()
        song_title = record.get('song_title')
        url = record.get('url')

        if record_mail == normalized_mail:
            liked_songs_list.append({
                'mail': mail,
                'song_title': song_title,
                'url': url
            })

    # Return the list of liked songs
    return liked_songs_list

def add_user_to_sheet(email, password):
    # Append the user data to the sheet
    sheet.append_row([email, password])
    # Open your Google Sheet

@app.route('/likesong', methods=['POST'])
def like_song():
    data = request.get_json()
    title = data.get('title')
    url = data.get('url')
    feed = 1
    mail = session['mail']
    favourites(mail,title,url,feed);
    return jsonify(success=True)    
    

@app.route('/likesonglist', methods=['GET'])
def likesonglist():
    mail = session['mail']
    print(mail)
    favourites = getfavourites(mail)
    print(favourites)
    return render_template('LikedSong.html', liked_songs=favourites)

@app.route('/first-time-user')
def first_time_user():
    return render_template('first-time-user.html')

@app.route('/logout')
def logout():
    # #
   session.pop('mail', None)
   return redirect("/")

@app.route('/home')
def landing():
    return render_template('Index.html')

@app.route('/search', methods=['GET'])
def searchonspotify():
    return render_template('SongList.html')
    
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    search_result = search_song_on_spotify(query)
    return jsonify(search_result)

# Load the KNN model and dataset
model_path = 'collaborative filtering/best_knn_model.pkl'
data_path = 'datasets/songs.csv'

df_songs = pd.read_csv(data_path)

# Convert user_id and song_id to category codes
df_songs['user_id_code'] = df_songs['user_id'].astype('category').cat.codes
df_songs['song_id_code'] = df_songs['song_id'].astype('category').cat.codes

# Check for any negative values in the codes
if (df_songs['user_id_code'] < 0).any() or (df_songs['song_id_code'] < 0).any():
    raise ValueError("Negative values found in user_id_code or song_id_code")

# Create the user-song interaction matrix
user_song_matrix = csr_matrix(
    (df_songs['listen_count'], (df_songs['user_id_code'], df_songs['song_id_code'])),
    shape=(df_songs['user_id_code'].nunique(), df_songs['song_id_code'].nunique())
)

def get_spotify_track_id(title, artist):
    try:
        results = sp.search(q=f'track:{title} artist:{artist}', type='track', limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['id']
        else:
            return None
    except Exception as e:
        print(f"Error retrieving Spotify ID for {title} by {artist}: {e}")
        return None


# Load the saved model at the start of your app
saved_model = joblib.load('../MusicRecommandationSystem/collaborative filtering/best_knn_model.pkl')

# Assuming df_songs has 'user_id_code', 'song_id_code', and 'listen_count'
user_song_matrix = df_songs.pivot(index='user_id_code', columns='song_id_code', values='listen_count').fillna(0)

# Convert the pivoted DataFrame to a CSR matrix
user_song_matrix_csr = csr_matrix(user_song_matrix.values)

def recommend_songs_random_user(n_neighbors=5, n_random=1):
    user_id = random.choice(df_songs['user_id'].unique())
    user_code = df_songs[df_songs['user_id'] == user_id]['user_id_code'].iloc[0]
    user_vector = user_song_matrix_csr[user_code]

    distances, indices = saved_model.kneighbors(user_vector, n_neighbors=n_neighbors)
    recommendations = []
    random_indices = random.sample(list(indices.flatten()), n_random)

    for index in random_indices:
        song_title = df_songs.iloc[index]['title']
        artist_name = df_songs.iloc[index]['artist_name']
        spotify_id = get_spotify_track_id(song_title, artist_name)
        if spotify_id:
            track = sp.track(spotify_id)
            recommendations.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            })
    
    return recommendations

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        recommendations = recommend_songs_random_user()
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_spotify_track_info(title, artist):
    try:
        results = sp.search(q=f'track:{title} artist:{artist}', type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            return {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'preview_url': track.get('preview_url'),
                'external_url': track['external_urls']['spotify']
            }
        else:
            return None
    except Exception as e:
        print(f"Error retrieving Spotify track info for {title} by {artist}: {e}")
        return None

def get_spotify_track_info(song_title, artist_name):
    spotify_id = get_spotify_track_id(song_title, artist_name)
    if spotify_id:
        track = sp.track(spotify_id)
        return {
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify']
        }
    return None

def recommend_songs_for_playlist(n_neighbors=5, n_songs=5):
    user_id = random.choice(df_songs['user_id'].unique())
    
    user_code = df_songs[df_songs['user_id'] == user_id]['user_id_code'].iloc[0]
    
    user_vector = user_song_matrix_csr[user_code]

    distances, indices = saved_model.kneighbors(user_vector, n_neighbors=n_neighbors)
    
    recommendations = []
    
    # Randomly select a subset of the nearest neighbors
    selected_indices = random.sample(list(indices.flatten()), n_songs)

    for index in selected_indices:
        song_title = df_songs.iloc[index]['title']
        artist_name = df_songs.iloc[index]['artist_name']
        track_info = get_spotify_track_info(song_title, artist_name)
        if track_info:
            recommendations.append(track_info)

    return recommendations

@app.route('/get_playlist_songs', methods=['POST'])
def get_playlist_songs():
    try:
        playlist_songs = recommend_songs_for_playlist()
        return jsonify(playlist_songs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/playlists')
def playlists():
    return render_template('playlists.html')

@app.route('/player')
def playler():
    return render_template('Players.html')

def get_spotify(title, artist):
    try:
        results = sp.search(q=f'track:{title} artist:{artist}', type='track', limit=10)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['id']
        else:
            return None
    except Exception as e:
        print(f"Error retrieving Spotify ID for {title} by {artist}: {e}")
        return None





# Set up Spotify API credentials
client_id = "380a6b3535dc420a905dccf328a0e165"
client_secret = "b0ca7947448246d28aafc40f49610cf4"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Load the image-based emotion detection model
processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")

# Create a pipeline for emotion detection
emotion_classifier = pipeline("image-classification", model=model, feature_extractor=processor)

# Define emotion to genre/characteristic mapping
emotion_to_genre = {
    'happy': ['pop', 'dance', 'electropop'],
    'sad': ['acoustic', 'blues', 'soul'],
    'angry': ['rock', 'metal', 'punk'],
    'neutral': ['jazz', 'classical', 'ambient'],
    'fear': ['dark', 'soundtrack', 'experimental'],
    'surprise': ['pop', 'alternative', 'indie'],
    'disgust': ['punk', 'grunge', 'hardcore']
}

# Capture image using cv2
def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam")
        return None

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        return None

    cap.release()

    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)

    return image_path

# Function to detect emotion from the image
def detect_emotion_from_image(image_path):
    image = Image.open(image_path)
    predictions = emotion_classifier(image)
    detected_emotion = predictions[0]['label'].lower()
    return detected_emotion

# Function to get songs for the detected emotion
def get_songs_for_emotion(emotion):
    if emotion in emotion_to_genre:
        genres = emotion_to_genre[emotion]
        genre_query = " ".join([f"genre:{genre}" for genre in genres])
        
        results = sp.search(q=genre_query, type='track', limit=20)
        tracks = results['tracks']['items']
        
        if not tracks:
            return None
        
        # Prepare data for the table
        songs_data = []
        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            spotify_link = track['external_urls']['spotify']
            
            # Append the track info to the songs_data list
            songs_data.append({
                "Track Name": track_name,
                "Artist": artist_name,
                "Album": album_name,
                "Spotify Link": spotify_link
            })
        
        # Convert the list of dictionaries to a DataFrame
        songs_df = pd.DataFrame(songs_data)
        return songs_df
    else:
        return None

@app.route('/mood')
def Mood():
    return render_template('Mood.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    image_path = capture_image()
    
    if image_path:
        detected_emotion = detect_emotion_from_image(image_path)
        print(f"Detected Emotion: {detected_emotion}")  # Debug print
        
        if detected_emotion:
            recommended_songs_df = get_songs_for_emotion(detected_emotion.lower())
            
            if recommended_songs_df is not None and not recommended_songs_df.empty:
                songs = recommended_songs_df.to_dict(orient='records')
                print(songs)  # Debug print
                return render_template('recommendation.html', emotion=detected_emotion.capitalize(), songs=songs)
    





if __name__ == '__main__':
    app.run(debug=True)
