# VENTURE

A full-stack music exploration platform that combines third-party music discovery, prompt-driven interaction, and a curated listening experience within a single, cohesive system. It is built with an emphasis on clean architecture, responsive user interaction, and production-oriented engineering practices.

The platform integrates external APIs, deterministic prompt interpretation, and custom audio playback into a unified experience, with an architecture designed to support scalability, accessibility, and AI-driven integrations without restructuring core components.

Try the Demo [here](https://venture-qgzz.onrender.com/).

## Table of Contents
- [What Does VENTURE Do?](#what-does-venture-do)
- [System Architecture](#system-architecture)
- [Core Components](#core-components)
- [Data and Control Flow](#data-and-control-flow)
- [Repository Structure](#repository-structure)
- [Future Improvements](#future-improvements)
- [Local Development](#local-development)
- [Configuration](#configuration)
- [License](#license)

## What Does VENTURE Do?

<img width="1120" height="599" alt="v1" src="https://github.com/user-attachments/assets/b36fdae7-86a5-4db1-b3c0-e73646ebcb19" />

VENTURE provides three primary user-facing experiences:

### 1. Spotify-Powered Music Search
A responsive search interface backed by the Spotify Web API that supports:

- Track, album, and artist search  
- Server-side authentication and token handling  
- Clean API normalization and validation  
- Debounced client-side input for low-latency UX

<img width="1120" height="599" alt="v2" src="https://github.com/user-attachments/assets/aa7e6094-f2a8-4d51-91d4-1aaf9fddf3a2" />

### 2. Mood and Theme Explorer
A prompt-driven exploration studio that:

- Accepts free-form natural language input  
- Interprets mood and theme keywords deterministically  
- Maps prompts to curated local audio samples  
- Dynamically updates background visuals for an immersive experience  

This feature functions as an AI-adjacent system today and as an AI integration surface tomorrow.

<img width="1120" height="599" alt="v3" src="https://github.com/user-attachments/assets/c4f7a400-3bcb-484e-bab8-1222a4153308" />

### 3. My Album: 14-Track Interactive Player
A fully designed album experience featuring:

- Fourteen curated audio tracks  
- Keyboard-accessible playback controls  
- Responsive layout optimized for desktop and mobile  
- Smooth transitions with minimal layout reflow

<img width="1120" height="599" alt="v4" src="https://github.com/user-attachments/assets/477e77fe-5d18-4a3f-a7d4-45684c4183ad" />

<img width="1120" height="599" alt="v5" src="https://github.com/user-attachments/assets/4b3431eb-1f68-4e7f-8854-5fb47746a1bb" />

## System Architecture

VENTURE follows a classic full-stack web architecture with clear separation of concerns and asynchronous extensibility.

### High-Level Architecture

```
┌──────────────────────────────┐
│       Client Interface       │
│     Django Templates + JS    │
│                              │
│  - Search UI                 │
│  - Explore Studio            │
│  - Album Player              │
│  - Keyboard Controls         │
└───────────────┬──────────────┘
                │ HTTP Requests
                ▼
┌──────────────────────────────┐
│       Application Layer      │
│            Django            │
│                              │
│  - URL Routing               │
│  - View Orchestration        │
│  - Input Validation          │
│  - Template Rendering        │
└───────────────┬──────────────┘
                │
                ▼
┌────────────────────────────────────────┐
│      Integration and Logic Layer       │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Spotify API Client               │  │
│  │ - Auth and token handling        │  │
│  │ - Search normalization           │  |
│  └──────────────────────────────────┘  │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Theme Mapping Engine             │  │
│  │ - Keyword and synonym matching   │  │
│  │ - Mood and genre selection       │  │
│  └──────────────────────────────────┘  │
└───────────────┬────────────────────────┘
                │
                ▼
┌──────────────────────────────┐
│     Static Asset Pipeline    │
│                              │
│  - Album audio tracks        │
│  - Mood sample clips         │
│  - Background images         │
│  - Styles and visuals        │
└──────────────────────────────┘
```

### Design Principles

- Server-rendered templates for predictable rendering and SEO friendliness  
- Lightweight JavaScript modules for interactivity and media control  
- Deterministic prompt interpretation over opaque ML dependencies  
- Asynchronous task infrastructure in place for future AI workloads  

## Core Components

### Backend

| Component | Responsibility |
|---------|----------------|
| `spotify_client` | Wrapper around Spotify Web API with auth, throttling, and normalized responses |
| `theme_mapping_engine` | Keyword-based interpreter mapping prompts to moods, visuals, and samples |
| `music` Django app | Search, Explore, Album views and orchestration |
| Background workers (RQ) | Non-blocking processing and future AI jobs |
| `ai_music` Django app | Scaffold for future inference modules |

### Frontend

| Component | Responsibility |
|---------|----------------|
| `player.js` | Keyboard-accessible album playback controller |
| `explore.js` | Prompt handling, background transitions, UI state |
| Django templates | Structured layout and server-rendered UI |

## Data and Control Flow

### Search Flow
1. User Input
2. Django View
3. Spotify API Wrapper
4. Normalized Results
5. Template Render

### Explore Flow
1. Prompt Text
2. Keyword Extraction
3. Theme Mapping
4. Background Selection + Audio Sample
5. UI Update

This design prioritizes a clean and understandable workflow, making it easy to debug and expand upon.

## Repository Structure

```
VENTURE/
├── manage.py                  # Django entrypoint
├── requirements.txt           # Python dependencies
├── render.yaml                # Deployment configuration
├── build.sh                   # Build script
├── README.md
├── LICENSE
│
├── venture_site/              # Django project configuration
│   ├── settings.py            # Global settings and static config
│   ├── urls.py                # Root URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── music/                     # Core application logic
│   ├── views.py               # Search, explore, album views
│   ├── urls.py                # App-level routing
│   ├── models.py              # Future expansion
│   ├── templates/music/       # UI templates
│   ├── static/music/          # JS, audio assets, visuals, styles
│   │   ├── album/             # 14-track album audio + artwork
│   │   ├── samples/           # Mood and theme audio samples
│   │   ├── bg/                # Background images
│   │   └── js/                # Client-side interaction logic
│   └── migrations/            # Django migrations
│
├── ai_music/                  # Forward-compatible AI module
│   ├── views.py
│   ├── urls.py
│   ├── templates/ai_music/
│   └── migrations/
```

## Local Development

### Prerequisites:
- Python 3.10 or higher
- pip
- Virtual environment tooling

### Setup
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The application runs at http://127.0.0.1:8000.

## Configuration

The system is configured entirely through environment variables.

For Example,
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
```

## Future Improvements

There are several high-value enhancements that could improve the project. These include:

1. **User Accounts + Playlists:** Allow users to save favourite samples, create mini-playlists, or bookmark moods as a natural extension that makes the app feel more like a personal music companion.

2. **Smarter Mood/Theme Inference:** Introduce a lightweight, explainable ML classifier for mood inference while still falling back to deterministic matching for reliability. This preserves robustness while allowing more expressive prompts. 

3. **Waveform Visualization:** Add a live, canvas-based waveform or spectrum visualization on the album player to potentially increase the multimedia feel of the interface.

## License

VENTURE is licensed under the MIT License.
