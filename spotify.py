import spotipy
from spotipy.oauth2 import SpotifyOAuth
from aio_util import to_async


def get_spotify(config: dict) -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-playback-state',
                                                     username='Chagan Sanathu',
                                                     client_id=config['spotify_client_id'],
                                                     client_secret=config['spotify_client_secret'],
                                                     redirect_uri='http://localhost:9999/',
                                                     open_browser=False))


@to_async
def get_now_playing_info(spotify: spotipy.Spotify):
    raw_playing_data = spotify.currently_playing()
    if raw_playing_data:
        if raw_playing_data['currently_playing_type'] == 'episode':
            raw_playing_data = spotify.currently_playing(additional_types='episode')
    return raw_playing_data


def get_playing_name(raw_playing_data: dict):
    if raw_playing_data['currently_playing_type'] == 'track':
        return f'{raw_playing_data["item"]["name"]} - {", ".join(i["name"] for i in raw_playing_data["item"]["artists"])}'
    else:
        return f'{raw_playing_data["item"]["name"]} - {raw_playing_data["item"]["show"]["name"]}'


def get_playing_url(raw_playing_data: dict):
    return raw_playing_data['item']['external_urls']['spotify']
