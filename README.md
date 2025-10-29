# 🎵 Sargam: Life’s cooler with a soundtrack.

## Overview

**Sargam** is a dynamic, Django-based web application that allows users to search for songs, discover music by genre, and explore albums and artists using the Spotify API. Designed with a clean, interactive interface and mobile responsiveness in mind, the app blends Python, JavaScript, and modern CSS to create an engaging experience that’s both functional and visually appealing.

Users can:

- Search for songs by title and view related albums and artists.

- Explore playlists across various genres like pop, classical, jazz, or hip-hop.

- Interact with floating space-themed animations and hover effects for a polished, immersive experience.

- Navigate seamlessly across the homepage, search, and exploration pages.

## Key features

- **Search:** search songs, artists, albums, etc. and display results with relevant information, 30 seconds preview (when available), and links to Spotify.

- **Album pages:** list tracks in the album, show album art, release date and link to Spotify.

- **Artist pages:** show artist details and top tracks (with preview playback).

- **Explore by genre:** fetches Spotify categories and displays playlists for a chosen genre.

- **Preserves search state:** “Back to Search” returns users to the previous query result.

- **Polished UI & UX:** responsive grid layout, hover animations, and canvas-based particle animations (subtle floating stars) for visual interest without sacrificing accessibility.

- **Security best practice:** Spotify credentials are stored in environment variables (.env) and never committed to source control.

- **Mobile responsive:** layouts and typography adapt to smaller screens; grids collapse to single-column on phones.

## Tech stack

- **Backend:** Django (views, URL routing, templates).

- **Frontend:** HTML, CSS (responsive grid, media queries), JavaScript for Canvas animations and UI enhancements.

- **API:** Spotify Web API (Client Credentials flow for server-side access).

- **HTTP client:** requests (Python) for server-to-Spotify communication.

- **Environment management:** python-dotenv (reads .env) + venv for local development.

- **Database:** SQLite (provided by Django for development).

- **Dev tooling:** VS Code, browser devtools (mobile emulation), Git for version control.

## Architecture

- Client (browser) requests a route.

- Django view receives the request and, if required, obtains a Spotify access token using server-side Client Credentials (credentials read from environment variables).

- Server → Spotify API: server makes authorized requests (search, album, artist, categories, playlists).

- Server parses the JSON response into compact objects and renders templates.

- Client displays results; JavaScript enhances visuals (Canvas background + small interactive pieces).

## How to Run Sargam Locally

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

## Future improvements

- Add user accounts and favorites (persisted model + auth).

- Use Spotify Web Playback SDK for authenticated playback.

- Add caching (Redis) for tokens and popular queries to reduce API usage.

- Accessibility improvements (aria attributes, high-contrast modes, keyboard navigation).

- End-to-end tests and automated deployment pipeline.