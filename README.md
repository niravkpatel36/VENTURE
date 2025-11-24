# 🎵 VENTURE: Life’s cooler with a soundtrack.

## Project overview
VENTURE is a lightweight music exploration and listening web application built with Django, designed as a portfolio-grade engineering project. It highlights several key capabilities:

- A search feature that integrates with the Spotify API for searching tracks, artists, and albums (used for the Search Music view).
- An Explore Music feature (the “Mood/Theme Studio”) that maps free-text prompts and mood/theme keywords to locally-hosted sample audio and dynamically updates the visual background for an immersive experience.
- A polished My Album feature that presents a full 14-track album with immersive album art, a compact player UI and accessible, keyboard-friendly controls.

The project purposefully balances visual polish and pragmatic engineering. Some parts are inspired by modern music apps such Apple Music and Spotify while remaining focused on what’s possible in a short, reliable MVP.

---

## Distinctiveness and Complexity

This project goes beyond a simple “music player” demo by combining multiple concerns that make it a stronger engineering artifact:

1. **Multimodal and reactive UX:** Instead of presenting a static list of audio files, VENTURE shifts the entire page’s visual mood to match the user’s input (mood keywords → background images) while playing context-appropriate samples. This blends audio, imagery, and UX design, turning a simple feature into an interactive visual-mood experience.

2. **Robust client-server mapping:** The explore feature processes a free-text prompt server-side using keyword and synonym matching (with a clean fallback to randomness). It returns stable static URLs for both the audio sample and the background image. 

This design avoids unnecessary ML dependencies, behaves consistently offline, and illustrates thoughtful engineering tradeoffs.

3. **Production-aware static assets handling:** All audio is served through Django static files, and the app includes graceful handling of missing directories or files. Instead of crashing, the UI fails softly and logs clear errors — a detail that matters in demo environments and makes the project production-aware.

4. **Polished UI and motion:** The project uses layered backgrounds, star animations, blur effects, and modals not just for aesthetics but for usability: maintaining contrast and readability across mood-based backgrounds. Achieving this required iterative CSS work and a light JS layer (e.g., handling autoplay restrictions with “Tap to play”).

**Complexity:**
- Integrates multiple subsystems (API interaction, deterministic AI-adjacent logic, visual/mood mapping, custom audio player).
- Demonstrates considered UX and accessibility, not just functional correctness.
- Features were built using resilient approaches, including but not limited to deterministic prompt mapping, static asset pipelines, and graceful fallbacks.

---

## Repository Structure

**Top-Level**
- **manage.py:** Django’s command-line utility for running the server and administrative tasks.
- **requirements.txt:** Python package dependencies.
- **db.sqlite3:** Local development database.

**Project Package: `venture_site/venture_site/`**
- **settings.py:** Global Django settings (installed apps, middleware, static files, auth, etc.).
- **urls.py:** Root URL configuration; includes app-level URL routing.
- **wsgi.py / asgi.py:** Entry points for deployment (WSGI/ASGI servers).
- **__init__.py:** Marks this as a Python package.

**App: `music/`**
- **views.py:** All core views:
    - Spotify search handler
    - Explore/Mood Studio handler
    - Author Album player
    - The deterministic mood-mapping logic
- **urls.py:** Routes for /search/, /explore/, /album/, and API endpoints.

**Templates**
- **music/templates/music/:** Includes layout.html, index.html, explore.html, album.html, and more to define page structure, display dynamic content, and extend shared layouts.

**Static Files**
- **music/static/music/:** Includes album/, bg/, js/, samples/, and styles.css to support the UI with styling, media assets, and client-side functionality.

**Other**
- **.env:** Environment variables (e.g., Spotify API credentials).
- **.gitignore:** Git ignore rules.
- **README.md:** Project documentation.

---

## How to Run VENTURE Locally

1. Clone the repository and enter the project folder.

git clone <your_repo_url>
cd venture_site

2. Create & activate a virtual environment:

*Windows (PowerShell):*
python -m venv venv
. .\venv\Scripts\Activate

*macOS / Linux:*
python3 -m venv venv
source venv/bin/activate

Install dependencies: pip install -r requirements.txt

3. Create a .env in the project root:

SPOTIFY_CLIENT_ID=your_id_here
SPOTIFY_CLIENT_SECRET=your_secret_here

4. Run the server: python manage.py runserver

5. Visit http://127.0.0.1:8000/. 

## Future Improvements

There are several high-value enhancements that could improve the project. These include:

1. **User Accounts + Playlists:** Allow users to save favourite samples, create mini-playlists, or bookmark moods as a natural extension that makes the app feel more like a personal music companion.

2. **Smarter Mood/Theme Inference:** Introduce a lightweight, explainable ML classifier for mood inference while still falling back to deterministic matching for reliability. This preserves robustness while allowing more expressive prompts. 

3. **Waveform Visualization:** Add a live, canvas-based waveform or spectrum visualization on the album player to potentially increase the multimedia feel of the interface.