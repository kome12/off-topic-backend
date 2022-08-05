import json
import os
import requests
from requests.auth import HTTPBasicAuth

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"
DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 20


def get_spotify_token():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    secret = os.environ['SPOTIFY_CLIENT_SECRET']

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = "grant_type=client_credentials"
    basic_auth = HTTPBasicAuth(client_id, secret)

    response = requests.request("POST", SPOTIFY_TOKEN_URL, headers=headers, data=payload, auth=basic_auth)

    if response.status_code >= 400 and response.status_code <= 500:
        raise Exception("Error in getting spotify token")

    token_object = response.json()
    return token_object.get('access_token')


def create_header(access_token):
    return {
        'Authorization': f'Bearer {access_token}'
    }


def create_url(spotify_id, market="JP", offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
    return f'{SPOTIFY_BASE_URL}shows/{spotify_id}/episodes?market={market}&offset={offset}&limit={limit}';


def call_spotify_episodes(url, headers):
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_spotify_episodes(spotify_id, market="JP", offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
    access_token = get_spotify_token()

    url = create_url(spotify_id, market, offset, limit)
    headers = create_header(access_token)

    return call_spotify_episodes(url, headers)

    
def get_all_spotify_episodes(spotify_id, market="JP"):
    access_token = get_spotify_token()
    headers = create_header(access_token)

    has_more_episodes = True
    offset = DEFAULT_OFFSET
    limit = DEFAULT_LIMIT
    all_episodes = []

    while has_more_episodes:
        url = create_url(spotify_id, market, offset, limit)
        response = call_spotify_episodes(url, headers)

        if response.get("total") > limit + offset:
            offset += limit
        else:
            has_more_episodes = False
        
        episodes = response.get("items")
        if episodes:
            all_episodes += episodes

    return all_episodes