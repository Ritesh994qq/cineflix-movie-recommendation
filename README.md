# CINEFLIX — Movie Recommendation System

A Netflix-inspired movie and TV series discovery dashboard built with Python, Streamlit, and custom CSS.

## Features
- Dark cinematic interface with responsive CSS
- 32 movies and TV series in a demo catalogue
- Search titles, genres, tags, and media type
- Filter by genre and browse Movies, TV Series, Top Rated, Trending, and My List
- Sort by rating, release year, or title
- Recommendation sections and detail panel
- Add/remove titles from My List (session-only)

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Optional: create and activate a virtual environment.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   streamlit run app.py
   ```
6. Open the local URL shown in the terminal (normally http://localhost:8501).

## Notes
- An internet connection is needed to load remote poster artwork.
- This is a recommendation/discovery demo, not a streaming service. The Watch Now action is intentionally a placeholder.
- The included catalogue and poster paths are sample data. For a production app, use a licensed data source/API and verify all image URLs.
- My List is stored in Streamlit session state and is not persisted after the session ends.
