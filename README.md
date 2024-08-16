# Music Recommendation System

This is a Music Recommendation System that integrates various recommendation algorithms (Collaborative Filtering, Content-based Filtering) and a mood-based recommendation system using facial emotion recognition. The system is built with Flask for the backend and uses the Spotify API to fetch songs.

## Features

1. **User Authentication**: Users can sign up, log in, and log out. Credentials are stored in a Google Sheets document.
2. **Song Search**: Users can search for songs on Spotify by title and artist.
3. **Song Recommendations**:
   - **Collaborative Filtering**: Based on the user's listening history.
   - **Content-based Filtering**: Recommends songs similar to those the user has liked in the past.
   - **Mood-based Recommendations**: Uses the user's facial expression (captured via webcam) to recommend songs that match the detected mood.
4. **Favorites**: Users can save their favorite songs, which are stored in Google Sheets.
5. **Playlist Generation**: Generates a playlist of songs based on user preferences and listening history.

## Technologies Used

- **Backend**: Flask
- **Machine Learning**: scikit-learn, transformers (for emotion detection)
- **APIs**: Spotify API, Google Sheets API
- **Webcam Integration**: OpenCV for capturing images
- **Emotion Detection**: Hugging Face's transformers for facial emotion classification
- **Database**: Google Sheets


