# VENTURE

A full-stack music exploration platform that combines third-party music discovery, prompt-driven interaction, and a curated listening experience within a single, cohesive system. It is built with an emphasis on clean architecture, responsive user interaction, and production-oriented engineering practices.

The platform integrates external APIs, deterministic prompt interpretation, and custom audio playback into a unified experience, with an architecture designed to support scalability, accessibility, and AI-driven integrations without restructuring core components.

Try the Demo [here](https://venture-qgzz.onrender.com/).

## What Does VENTURE Do?

VENTURE provides three primary user-facing experiences:

### 1. Spotify-Powered Music Search
A responsive search interface backed by the Spotify Web API that supports:

- Track, album, and artist search  
- Server-side authentication and token handling  
- Clean API normalization and validation  
- Debounced client-side input for low-latency UX  

### 2. Mood and Theme Explorer
A prompt-driven exploration studio that:

- Accepts free-form natural language input  
- Interprets mood and theme keywords deterministically  
- Maps prompts to curated local audio samples  
- Dynamically updates background visuals for an immersive experience  

This feature functions as an AI-adjacent system today and as an AI integration surface tomorrow.

### 3. My Album: 14-Track Interactive Player
A fully designed album experience featuring:

- Fourteen curated audio tracks  
- Keyboard-accessible playback controls  
- Responsive layout optimized for desktop and mobile  
- Smooth transitions with minimal layout reflow  

## System Architecture

VENTURE follows a classic full-stack web architecture with clear separation of concerns and asynchronous extensibility.

### High-Level Architecture

<img width="600" height="600" alt="architecture" src="https://github.com/user-attachments/assets/781fa329-0aea-46ff-9290-267d8d0675ee" />

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

<img width="600" height="600" alt="Repo Structure" src="https://github.com/user-attachments/assets/beddf554-c015-4b8d-8e11-635971f7149b" />

## Future Improvements

There are several high-value enhancements that could improve the project. These include:

1. **User Accounts + Playlists:** Allow users to save favourite samples, create mini-playlists, or bookmark moods as a natural extension that makes the app feel more like a personal music companion.

2. **Smarter Mood/Theme Inference:** Introduce a lightweight, explainable ML classifier for mood inference while still falling back to deterministic matching for reliability. This preserves robustness while allowing more expressive prompts. 

3. **Waveform Visualization:** Add a live, canvas-based waveform or spectrum visualization on the album player to potentially increase the multimedia feel of the interface.

## License

VENTURE is licensed under the MIT License.
