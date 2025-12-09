# music/views.py
import os, random
import base64
import requests
from dotenv import load_dotenv

from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

load_dotenv()

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_ALBUM_URL = "https://api.spotify.com/v1/albums/"
SPOTIFY_ARTIST_URL = "https://api.spotify.com/v1/artists/"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, "static", "music", "samples")

# ---------- Basic pages ----------
def home_page(request):
    return render(request, "music/home.html")

@cache_page(5)
def home(request):
    """
    Search page for Spotify-backed search.
    Query param: q
    """
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

# ---------- Spotify helpers ----------
def get_spotify_token():
    """Obtain a Spotify access token (Client Credentials)."""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in environment.")

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

# ---------- Album / Artist ----------
def album_detail(request, album_id):
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

# ---------- Explore (genres/categories) ----------
def explore(request):
    """Show Spotify categories (genres). Fallback to static list if the call fails."""
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get("https://api.spotify.com/v1/browse/categories?country=US&limit=12", headers=headers, timeout=10)
        resp.raise_for_status()
        categories = resp.json().get("categories", {}).get("items", [])
    except Exception as e:
        categories = [
            {"id": "pop", "name": "Pop", "icons": [{"url": static("music/img/genres/pop.jpg")}]},
            {"id": "indie", "name": "Indie", "icons": [{"url": static("music/img/genres/indie.jpg")}]},
            {"id": "lofi", "name": "Lo-Fi", "icons": [{"url": static("music/img/genres/lofi.jpg")}]},
            {"id": "jazz", "name": "Jazz", "icons": [{"url": static("music/img/genres/jazz.jpg")}]},
        ]
    return render(request, "music/explore.html", {"categories": categories})

def explore_genre(request, genre_id):
    """Fetch and display playlists for a specific genre/category (Spotify)."""
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://api.spotify.com/v1/browse/categories/{genre_id}/playlists"
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        data = {"playlists": {"items": []}}
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
    """Alias for explore_genre (keeps compatibility with templates)."""
    return explore_genre(request, genre_id)

# ---------- Generate page placeholder ----------
def generate(request):
    return render(request, "music/generate.html")

# ---------- AI Studio (local sample mixing) ----------
@csrf_exempt
def ai_view(request):
    """
    Render the Explore Music page (space-themed).
    """
    return render(request, "music/explore.html", {})

logger = logging.getLogger(__name__)

# === Mood → Background Image Map ===
MOOD_BG = {
    "autumn": "music/bg/Autumn.jpg",
    "spring": "music/bg/Spring.jpg",
    "summer": "music/bg/Summer.jpg",
    "winter": "music/bg/Winter.jpg",
    "crazy": "music/bg/Crazy.jpg",
    "day": "music/bg/Day.jpg",
    "melancholy": "music/bg/Melancholy.jpg",
    "night": "music/bg/Night.jpg",
    "peace": "music/bg/Peace.jpg",
}

@csrf_exempt
def ai_generate_api(request):
    """
    POST endpoint: accepts 'prompt' (mood/vibe)
    Returns JSON: { success: True, file: "<static url>", chosen_sample: "<filename>", mood: "<prompt>", background: "<bg>" }
    """
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Only POST allowed"}, status=405)

        prompt_raw = (request.POST.get("prompt") or "").strip()
        prompt = prompt_raw.lower()

        if not prompt:
            return JsonResponse({"error": "Missing prompt"}, status=400)

        base_dir = os.path.join(os.path.dirname(__file__), "static", "music", "samples")
        if not os.path.isdir(base_dir):
            logger.error("Samples directory missing: %s", base_dir)
            return JsonResponse({"error": "Server misconfiguration: samples directory missing."}, status=500)

        # mood -> sample mapping
        mood_map = {
            "autumn": ["Autumn.mp3"],
            "spring": ["Spring.mp3"],
            "summer": ["Summer.mp3"],
            "winter": ["Winter.mp3"],
            "crazy": ["Crazy.mp3"],
            "day": ["Day.mp3"],
            "melancholy": ["Melancholy.mp3"],
            "night": ["Night.mp3"],
            "peace": ["Peace.mp3"],
        }

        # semantic synonyms
        semantic_map = {
            "summer": ["beach", "california", "sun", "heat", "tropical", "warm"],
            "winter": ["snow", "cold", "frost", "december", "christmas", "icy"],
            "autumn": ["fall", "leaves", "pumpkin", "november", "autumn"],
            "spring": ["flowers", "valley", "nice", "jazz"],
            "peace": ["calm", "relax", "zen", "quiet", "peace"],
            "melancholy": ["sad", "nostalgia", "rain", "blue", "melancholy"],
            "crazy": ["party", "wild", "energetic", "rave", "locked in", "adrenaline"],
            "day": ["dope", "skateboard", "fun", "confident", "type shi", "good", "life", "chill"],
            "night": ["late", "night", "midnight", "stars", "nocturnal"]
        }

        # 1) direct mood match
        matched_files = []
        chosen_mood = None
        for key, files in mood_map.items():
            if key in prompt:
                matched_files = [f for f in files if os.path.exists(os.path.join(base_dir, f))]
                chosen_mood = key
                break

        # 2) synonyms match
        if not matched_files:
            for key, syns in semantic_map.items():
                for s in syns:
                    if s in prompt:
                        matched_files = [f for f in mood_map.get(key, []) if os.path.exists(os.path.join(base_dir, f))]
                        chosen_mood = key
                        break
                if matched_files:
                    break

        # 3) fallback random audio sample
        if not matched_files:
            all_samples = [f for f in os.listdir(base_dir) if f.lower().endswith(('.mp3', '.wav'))]
            if not all_samples:
                logger.error("No sample audio files present in %s", base_dir)
                return JsonResponse({"error": "No sample audio files on server."}, status=500)
            chosen = random.choice(all_samples)
            chosen_mood = None
        else:
            chosen = random.choice(matched_files)

        file_url = static(f"music/samples/{chosen}")

        bg_dir = os.path.join(os.path.dirname(__file__), "static", "music", "bg")
        random_bg = "music/bg/Day.jpg"

        if os.path.isdir(bg_dir):
            bg_files = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if bg_files:
                random_bg = f"music/bg/{random.choice(bg_files)}"

        if chosen_mood and chosen_mood in MOOD_BG:
            bg_url = static(MOOD_BG[chosen_mood])
        else:
            bg_url = static(random_bg)

        return JsonResponse({
            "success": True,
            "file": file_url,
            "mood": prompt_raw,
            "chosen_sample": chosen,
            "background": bg_url
        })

    except Exception as e:
        logger.exception("ai_generate_api failed")
        return JsonResponse({"error": "Internal server error", "details": str(e)}, status=500)


def author_album(request):
    """
    Serve the author's album page. Expects files in:
      music/static/music/album/
    and album art at music/static/music/album/Album Cover - Postscript.png
    """
    try:
        album_dir = os.path.join(os.path.dirname(__file__), "static", "music", "album")
        if not os.path.isdir(album_dir):
            return render(request, "music/album.html", {"album_tracks": [], "album_art": None, "message": "Album not found.", "album_title": "From the Artist"})

        filename_to_title = {
            "Sainted.wav": "Sainted",
            "Nocturnal_Vision.wav": "Nocturnal Vision",
            "Righteous_Liars.wav": "Righteous Liars",
            "Hold_On_2.wav": "Hold On",
            "Arson (1).wav": "Arson",
            "Pyromania.wav": "Pyromania",
            "FE_Draft_Final (5).wav": "Fake Entitlement",
            "Allegiance.wav": "Allegiance",
            "Kingda Ka.wav": "Kingda Ka",
            "Graffiti.wav": "Graffiti",
            "Tribulations_1 (2).wav": "Tribulations",
            "Epiphany_Pt_1.wav": "Epiphany",
            "Scripted.wav": "Scripted",
            "Leaf.wav": "Leaf",
        }

        ordered_filenames = [
            "Sainted.wav",
            "Nocturnal_Vision.wav",
            "Righteous_Liars.wav",
            "Hold_On_2.wav",
            "Arson (1).wav",
            "Pyromania.wav",
            "FE_Draft_Final (5).wav",
            "Allegiance.wav",
            "Kingda Ka.wav",
            "Graffiti.wav",
            "Tribulations_1 (2).wav",
            "Epiphany_Pt_1.wav",
            "Scripted.wav",
            "Leaf.wav",
        ]

        album_tracks = []
        for fname in ordered_filenames:
            disk_path = os.path.join(album_dir, fname)
            if os.path.exists(disk_path):
                display = filename_to_title.get(fname, fname)
                album_tracks.append({"title": display, "file": static(f"music/album/{fname}")})

        art_path = os.path.join(album_dir, "Album Cover - Postscript.png")
        album_art = static("music/album/Album Cover - Postscript.png") if os.path.exists(art_path) else None

        return render(request, "music/album.html", {
            "album_tracks": album_tracks,
            "album_art": album_art,
            "message": None,
            "album_title": "POSTSCRIPT"
        })
    except Exception as e:
        logger.exception("author_album failed")
        return render(request, "music/album.html", {"album_tracks": [], "album_art": None, "message": "Server error loading album.", "album_title": "POSTSCRIPT"})
    
    