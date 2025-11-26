# 🎵 VENTURE: Life’s cooler with a soundtrack.

## Table of Contents

- [Project Overview](#project-overview)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
  - [Why VENTURE Is Distinct](#why-venture-is-distinct)
  - [Why VENTURE Is Complex](#why-venture-is-complex)
- [Repository Structure](#repository-structure)
- [How to Run VENTURE Locally](#how-to-run-venture-locally)
- [Screencast](#screencast)
- [Future Improvements](#future-improvements)

---

## Project overview
VENTURE is a full-stack Django web application designed to combine music exploration, mood-driven audio playback, Spotify search integration, and a custom album experience into one cohesive platform. The project intentionally balances engineering rigor with visual creativity, demonstrating the ability to integrate API interaction, server-side logic, JavaScript-based UI behavior, and static asset processing inside a modern Django architecture. It highlights several key capabilities:

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

### Why VENTURE Is Distinct

1. **Different from Project 4 (Network)**

Project 4 centers on user accounts, posts, followers, likes, and CRUD-based social interactions.
VENTURE focuses on multimedia transformation, mood interpretation, and external API integration; with:

- mood-based background and audio transformations,
- Spotify API search integration,
- deterministic prompt-to-media mapping,
- custom album interface,
- three separate experiences (Search, Explore, Album).

It solves a different category of problem and uses Django in a different way than a social platform.

2. **Different from Project 2 (Commerce)**

Project 2 implements listings, bids, categories, watchlists, and transactional workflows.
VENTURE contains no commerce or listing system.

Its complexity instead comes from:

- multimedia handling,
- prompt parsing,
- mood inference,
- static asset orchestration,
- layered UI/UX behavior.

So while Project 2 is centered on items and transactions, VENTURE is centered on media transformation and user experience.

3. **Different from Projects 1 & 3 (Wiki & Mail)**

Projects 1 and 3 emphasize front-end interaction and traditional Django features (forms, editing, email logic).
VENTURE differs because several core behaviors must run server-side:

- deterministic mapping of prompts → audio + background,
- server-side Spotify API communication,
- rendering dynamic media assets,
- a Django model storing custom album track data.

Combined with modal UI, custom audio controls, and dynamic scripted behavior, VENTURE operates across multiple layers of the stack in ways those projects do not attempt.

### Why VENTURE Is Complex

1. **Deterministic Mood/Theme Engine**

The Explore feature uses a custom, deterministic mapping algorithm that:

- parses user free-text,
- matches keywords and synonyms,
- assigns a corresponding mood background image,
- selects context-appropriate audio samples,
- falls back gracefully when ambiguous or unknown prompts are provided.

This intentionally avoids black-box machine learning while still providing “AI-adjacent” behavior through thoughtful engineering tradeoffs. It behaves consistently even offline and illustrates robust server-side design.

2. **Robust Client-Server Interaction**

VENTURE uses a hybrid approach where:

- prompts are interpreted on the server,
- background images and audio samples are served via Django static file URLs,
- the UI reacts to those computed values in real-time.

3. **Spotify Search Integration**

The Search feature communicates directly with the Spotify Web API, enabling queries for:

- tracks,
- artists,
- albums.

The app handles:

- OAuth token retrieval and storage on the server,
- token expiration recovery,
- dynamic routing (/artist/<id>/, /album/<id>/),
- graceful fallback when Spotify returns incomplete data.

4. **A Fully Custom Album Experience**

VENTURE includes a polished "My Album" page that:

- displays a 14-track original album with tracklist,
- renders layered backgrounds and visual effects,
- includes a custom, responsive audio player,
- supports keyboard navigation,
- enlarges album art with a modal powered by JavaScript,
- allows closing the modal by clicking outside,
- synchronizes UI state with the currently playing track.

5. **Multimodal and Reactive UX**

VENTURE blends imagery, motion, animation, and audio to create a reactive environment:

- layered backgrounds,
- subtle star animations,
- controllable blur/contrast filters for readability,
- “Tap to Play” behavior to comply with mobile autoplay restrictions,
- UI that shifts visuals based on mood input.

This required iterative CSS tuning and a light but purposeful JavaScript layer.

6. **Production-Aware Static Asset Handling**

All media is served via Django’s static pipeline. The app includes:

- checks for missing audio/image directories,
- safe fallback assets,
- clear logging to avoid silent failures,
- consistent URL generation across environments.

7. **Fully Mobile-Responsive UI**

The UI is intentionally responsive:

- audio controls reflow on small screens,
- modal interactions are touch-friendly,
- mood backgrounds scale correctly,
- album layout collapses elegantly on mobile.

**Overall Summary**

VENTURE demonstrates complexity across:

- multimodal UX design,
- deterministic AI-style logic without ML,
- full-stack API workflows,
- dynamic Django view logic,
- multimedia processing,
- advanced template usage,
- JavaScript-driven interactivity,
- responsive design,
- robust static asset pipelines.

---

## Repository Structure

**Top-Level**
- **manage.py:** Django’s command-line utility for running the server and administrative tasks.
- **requirements.txt:** Python package dependencies.
- **db.sqlite3:** Local development database.
- **.env:** Environment variables (e.g., Spotify API credentials).
- **.gitignore:** Git ignore rules.
- **README.md:** Project documentation.

**Django Project: `venture_site/venture_site/`**
- **settings.py:**
    - Installed apps
    - Static files configuration
    - Environment variables (Spotify)
    - Template directories

- **urls.py:**
    - Root URL configuration
    - Includes the `music` app routes

- **wsgi.py / asgi.py:**
    - Deployment entry points

**Django App: `music/`**
- **models.py:** Album track model including:
    - title
    - track number
    - audio file path
    - duration
    - metadata

Uses Django ORM for persistent data.

- **views.py:** Core back-end logic, including:
    - Spotify search
    - Artist detail view
    - Album detail view
    - Deterministic mood-mapping engine
    - Explore Music processing
    - Album track loader and audio controller

- **urls.py:** Routes for:
    - `/search/`
    - `/explore/`
    - `/album/`
    - `/artist/<id>/`
    - `/album/<id>/`

**Templates: `music/templates/music/`**
- **layout.html:** Shared layout, navbar, footer.
- **index.html:** Landing page.
- **search.html:** Spotify search UI.
- **artist_detail.html / album_detail.html:** Dynamic metadata displays.
- **explore.html:** Mood-based background + sample audio.
- **album.html** Custom album player with modal and interactions.

**Static Files: `music/static/music/`**
- **styles.css:**
    - responsive layouts
    - layered backgrounds
    - animations
    - custom audio UI styling

- **js/:**
    - modal logic
    - interactive album behavior
    - explore-page scripts

- **bg/, album/, samples/:**
    - background images
    - album artwork
    - track audio samples

---

## How to Run VENTURE Locally

1. Clone the repository and enter the project folder.

    - git clone <your_repo_url>

    - cd venture_site

2. Create & activate a virtual environment:

    - Windows (PowerShell):
      
      python -m venv venv
      
      . .\venv\Scripts\Activate

    - macOS / Linux:
      
      python3 -m venv venv
      
      source venv/bin/activate

    - Install dependencies: pip install -r requirements.txt

3. Create a .env in the project root:

    - SPOTIFY_CLIENT_ID=your_id_here
    - SPOTIFY_CLIENT_SECRET=your_secret_here

4. Run the server: python manage.py runserver

5. Visit http://127.0.0.1:8000/.

## Screencast
A demonstration video showcasing the above mentioned features is available here: [Click Here to See Demo](https://www.youtube.com/watch?v=pQnOPU1NGog)

## Future Improvements

There are several high-value enhancements that could improve the project. These include:

1. **User Accounts + Playlists:** Allow users to save favourite samples, create mini-playlists, or bookmark moods as a natural extension that makes the app feel more like a personal music companion.

2. **Smarter Mood/Theme Inference:** Introduce a lightweight, explainable ML classifier for mood inference while still falling back to deterministic matching for reliability. This preserves robustness while allowing more expressive prompts. 

3. **Waveform Visualization:** Add a live, canvas-based waveform or spectrum visualization on the album player to potentially increase the multimedia feel of the interface.