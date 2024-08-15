from flask import Flask, render_template, request, jsonify, render_template, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import random
import pandas as pd
from scipy.sparse import csr_matrix
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__, static_folder='Content')


#Harjot Changes
app.secret_key = "2dcf15dcc7d5ec9958ceb1c2a6bc249e9b774f5538ae83e6"  # Set your secret key here

# Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("credentials").sheet1


##

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
        return render_template('login.html')  # Ensure you have this template

@app.route('/login', methods=['POST'])
def login():
    print("second")
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        print(f"Received mail: {mail}, password: {password}")
        users = get_users_from_sheet()
        print(f"Users from sheet: {users}")
        if mail in users:
            stored_password = str(users.get(mail)).strip()  # Convert stored password to string
            print(f"Stored password for '{mail}': '{stored_password}'")
            if stored_password == password:
                print(f"Password matches for mail: {mail}")
                session['mail'] = mail
                return redirect(url_for('landing'))
            else:
                print(f"Password does not match for mail: {mail}")
                return render_template('login.html', error='Invalid credentials')
        else:
            print(f"mail {mail} not found in users")
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/first-time-user')
def first_time_user():
    return render_template('first-time-user.html')

@app.route('/logout')
def logout():
    session.pop('mail', None)
    return redirect(url_for('login'))

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

if __name__ == '__main__':
    app.run(debug=True)
