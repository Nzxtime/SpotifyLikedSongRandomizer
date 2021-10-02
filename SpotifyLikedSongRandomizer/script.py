import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from os import path
import datetime
import random


class SpotifyLikedSongRandomizer():
    for location in path.expanduser(
            "~/.config/spotify-liked-song-randomizer/"), "/etc/spotify-liked-song-randomizer/":
        try:
            with open(path.join(location, "config.json")) as source:
                data = json.load(source)

        except IOError:
            pass

    if data is None:
        print('Create a config.json file in the following directory:')
        print(path.abspath(
            path.expanduser(
                "~/.config/spotify-liked-song-randomizer/")) + ' or /etc/spotify-liked-song-randomizer/')
        print('Use the config.json.example as a reference.')
        print('For further information visit https://github.com/Nzxtime/SpotifyLikedSongRandomizer')
        exit()

    scope = 'playlist-modify-public playlist-modify-private user-read-currently-playing user-read-playback-state ' \
            'user-modify-playback-state user-library-read'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=data['spotify']['spotify_username'], scope=scope,
                                                   client_id=data['spotify']['spotify_client_id'],
                                                   client_secret=data['spotify']['spotify_client_secret'],
                                                   redirect_uri=data['spotify']['spotify_redirect_uri']))

    def get_all_liked_songs(self):
        print(self.sp.current_user_saved_tracks())

    def check_for_playlist_name(self, results):
        for playlist in results['items']:
            if "RandomizedLikedSongs" in playlist['name']:
                self.sp.current_user_unfollow_playlist(playlist['id'])
                break

    def get_playlist_id(self):
        self.playlist_id = None
        results = self.sp.current_user_playlists()
        self.check_for_playlist_name(results)

        while results['next']:
            results = self.sp.next(results)
            self.check_for_playlist_name(results)

        if self.playlist_id is None:
            date = datetime.date.today()
            name = f'RandomizedLikedSongs {str(date.day)}.{str(date.month)}.{str(date.year)}'
            playlist = self.sp.user_playlist_create(user=self.sp.current_user()["id"], name=name)
            self.playlist_id = playlist['id']

    def get_current_liked_tracks(self):
        results = self.sp.current_user_saved_tracks()
        songs = results['items']

        while results['next']:
            results = self.sp.next(results)
            songs.extend(results['items'])

        random.shuffle(songs)

        self.add_tracks(songs)

    def add_tracks(self, results):
        for idx in range(0, len(results), 100):
            uris = [item['track']['uri'] for item in results[idx:idx + 100]]
            self.sp.playlist_add_items(self.playlist_id, uris)


if __name__ == '__main__':
    randomizer = SpotifyLikedSongRandomizer()
    randomizer.get_playlist_id()
    randomizer.get_current_liked_tracks()
    print(f'Created playlist')
