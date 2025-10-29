import os
import base64
import requests
from dotenv import load_dotenv
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.cache import cache_page

load_dotenv()

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_ALBUM_URL = "https://api.spotify.com/v1/albums/"
SPOTIFY_ARTIST_URL = "https://api.spotify.com/v1/artists/"

def home_page(request):
    return render(request, "music/home.html")

def get_spotify_token():
    """Obtain a Spotify access token using Client Credentials flow."""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as environment variables.")

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    data = {"grant_type": "client_credentials"}
    resp = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data, timeout=10)
    resp.raise_for_status()
    token = resp.json().get("access_token")
    return token

def search_spotify(query, token, limit=10):
    """Search Spotify for tracks and return parsed results."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": limit}
    resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    tracks = []
    for item in data.get("tracks", {}).get("items", []):
        track = {
            "name": item.get("name"),
            "artists": ", ".join([a.get("name") for a in item.get("artists", [])]),
            "artist_id": item.get("artists", [{}])[0].get("id"),
            "album_name": item.get("album", {}).get("name"),
            "album_id": item.get("album", {}).get("id"),
            "album_image": (item.get("album", {}).get("images") or [{}])[0].get("url"),
            "preview_url": item.get("preview_url"),
            "spotify_url": item.get("external_urls", {}).get("spotify"),
        }
        tracks.append(track)
    return tracks

@cache_page(5)
def home(request):
    query = request.GET.get("q", "").strip()
    results = None
    error = None

    if query:
        try:
            token = get_spotify_token()
            results = search_spotify(query, token, limit=12)
        except Exception as e:
            error = str(e)

    return render(request, "music/index.html", {
        "query": query,
        "results": results,
        "error": error,
    })

def album_detail(request, album_id):
    """Display details and track list for a specific album."""
    query = request.GET.get("q", "")
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{SPOTIFY_ALBUM_URL}{album_id}", headers=headers, timeout=10)
        resp.raise_for_status()
        album = resp.json()
    except Exception as e:
        return render(request, "music/error.html", {"error": str(e)})

    return render(request, "music/album_detail.html", {
        "album": album,
        "query": query,
    })

def artist_detail(request, artist_id):
    """Display artist info and their top tracks."""
    query = request.GET.get("q", "")
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        artist_resp = requests.get(f"{SPOTIFY_ARTIST_URL}{artist_id}", headers=headers, timeout=10)
        top_tracks_resp = requests.get(
            f"{SPOTIFY_ARTIST_URL}{artist_id}/top-tracks?market=US", headers=headers, timeout=10
        )

        artist_resp.raise_for_status()
        top_tracks_resp.raise_for_status()

        artist = artist_resp.json()
        top_tracks = top_tracks_resp.json().get("tracks", [])
    except Exception as e:
        return render(request, "music/error.html", {"error": str(e)})

    return render(request, "music/artist_detail.html", {
        "artist": artist,
        "top_tracks": top_tracks,
        "query": query,
    })

def explore(request):
    """Show Spotify categories (genres)."""
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get("https://api.spotify.com/v1/browse/categories?country=US&limit=12", headers=headers, timeout=10)
        resp.raise_for_status()
        categories = resp.json().get("categories", {}).get("items", [])
    except Exception as e:
        categories = []
        error = str(e)
    return render(request, "music/explore.html", {"categories": categories})

def explore_genre(request, genre_id):
    """Fetch and display playlists for a specific genre."""
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"https://api.spotify.com/v1/browse/categories/{genre_id}/playlists"
    resp = requests.get(url, headers=headers)
    data = resp.json()

    playlists = []
    for item in data.get("playlists", {}).get("items", []):
        playlists.append({
            "name": item.get("name"),
            "image": (item.get("images") or [{}])[0].get("url"),
            "spotify_url": item.get("external_urls", {}).get("spotify"),
        })

    return render(request, "music/explore_genre.html", {
        "playlists": playlists,
        "genre_id": genre_id,
    })


def genre_detail(request, genre_id):
    """Show popular playlists for a given Spotify genre category."""
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://api.spotify.com/v1/browse/categories/{genre_id}/playlists?country=US&limit=10"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        playlists = resp.json().get("playlists", {}).get("items", [])
    except Exception as e:
        playlists = []
        error = str(e)
    return render(request, "music/genre_detail.html", {
        "playlists": playlists,
        "genre_id": genre_id,
    })

