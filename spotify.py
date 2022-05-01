import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# MOOD OPTIONS: low, medium, party
LOW_MIN_COUNT = 0
MEDIUM_MIN_COUNT = 1
PARTY_MIN_COUNT = 2

LOW_VOL = 30
MED_VOL = 70
PARTY_VOL = 100

# Lofi
LOW_PLAYLIST_URL = 'https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn?si=a34f442bf71c42c4'
# Pop
MED_PLAYLIST_URL = 'https://open.spotify.com/playlist/37i9dQZF1DWUa8ZRTfalHk?si=a8218adb7374453b'
# Rap
PARTY_PLAYLIST_URL = 'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd?si=66cab474e9654e38'

class SpotifyManager:

    def __init__(self):
        self.scope = 'streaming'
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=self.scope))
        self.playlist = LOW_PLAYLIST_URL

    def change_playback(self, people_count):
        print('Current playlist set to ', self.playlist)
        print('Received count of ', people_count, ' playlist may update soon')

        playlist = ''
        vol = 0
        if (people_count >= PARTY_MIN_COUNT):
            playlist = PARTY_PLAYLIST_URL
            vol = PARTY_VOL
        elif (people_count >= MEDIUM_MIN_COUNT):
            playlist = MED_PLAYLIST_URL
            vol = MED_VOL
        else:
            playlist = LOW_PLAYLIST_URL
            vol = LOW_VOL

        if (playlist != self.playlist):
            self.playlist = playlist
            self.spotify.start_playback(context_uri=playlist, device_id=0)
            self.spotify.volume(volume_percent=vol)

    def stop_playback(self):
        self.spotify.pause_playback(device_id=0)


def get_mood(people_count):
    if (people_count >= PARTY_MIN_COUNT):
        return 'PARTY'
    elif (people_count >= MEDIUM_MIN_COUNT):
        return 'MED'
    else:
        return 'LOW'