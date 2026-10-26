import streamlit as st
from difflib import SequenceMatcher

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Cineflix | Discover Your Next Watch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Oswald:wght@500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 85% 0%, #321015 0%, #111014 30%, #08090b 70%);
    color: #f5f5f7;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8,9,11,0.9);
}

.block-container {
    max-width: 1500px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
    overflow: visible;
}

.brand {
    font-family: 'Oswald', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1.3;
    padding-top: 0.5rem;
    overflow: visible;
}

.brand {
    font-family: 'Oswald', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -1px;
}

.brand span {
    color: #e50914;
}

.tagline {
    color: #aaa;
    font-size: .75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero {
    border: 1px solid #292a30;
    border-radius: 22px;
    padding: 2.5rem;
    margin: 1.5rem 0;
    min-height: 300px;
    background:
        linear-gradient(90deg, #08090b 0%, rgba(8,9,11,.95) 45%, rgba(8,9,11,.25) 100%),
        url("https://image.tmdb.org/t/p/w1280/7I6VUdPj6tQec7K7Qy3g7mQ3Z6J.jpg")
        center/cover;
}

.hero-kicker {
    color: #ff3545;
    font-size: .8rem;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero h1 {
    font-family: 'Oswald', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    margin: .7rem 0;
    line-height: 1.1;
}

.hero p {
    color: #ddd;
    max-width: 650px;
    line-height: 1.7;
}

.pill {
    display: inline-block;
    border: 1px solid #4a4b52;
    border-radius: 20px;
    padding: 5px 12px;
    margin: 3px 5px 3px 0;
    background: #17181d;
    font-size: .8rem;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-top: 1.2rem;
}

.section-sub {
    color: #aaa;
    font-size: .85rem;
    margin-bottom: .8rem;
}

.movie-title {
    font-weight: 700;
    font-size: .95rem;
    margin-top: .5rem;
    min-height: 2.3rem;
    line-height: 1.3;
}

.movie-meta {
    color: #aaa;
    font-size: .78rem;
    margin-bottom: .5rem;
}

div[data-testid="stImage"] img {
    border-radius: 10px;
    border: 1px solid #303036;
    transition: transform .2s ease;
}

div[data-testid="stImage"] img:hover {
    transform: scale(1.03);
}

.stButton button {
    background: #191a20;
    color: white;
    border: 1px solid #393a41;
    border-radius: 9px;
    font-weight: 600;
}

.stButton button:hover {
    background: #e50914;
    border-color: #e50914;
    color: white;
}

div[data-testid="stTextInput"] input {
    background: #17181d;
    color: white;
    border-radius: 10px;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #17181d;
    color: white;
    border-radius: 10px;
}

hr {
    border-color: #292a30;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MOVIE DATABASE ----------------
MOVIES = [
    {"title":"The Batman","year":2022,"kind":"Movie","genre":"Action","rating":7.8,"duration":"2h 56m","poster":"https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg","overview":"Batman investigates corruption in Gotham City.","tags":"crime mystery detective dark"},
    {"title":"Interstellar","year":2014,"kind":"Movie","genre":"Sci-Fi","rating":8.7,"duration":"2h 49m","poster":"https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg","overview":"Explorers travel through space to find humanity a new home.","tags":"space science adventure emotional"},
    {"title":"Inception","year":2010,"kind":"Movie","genre":"Sci-Fi","rating":8.8,"duration":"2h 28m","poster":"https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg","overview":"A thief enters dreams to plant an idea in someone's mind.","tags":"mind thriller heist"},
    {"title":"The Dark Knight","year":2008,"kind":"Movie","genre":"Action","rating":9.0,"duration":"2h 32m","poster":"https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg","overview":"Batman faces the dangerous Joker in Gotham.","tags":"crime superhero detective"},
    {"title":"Dune: Part Two","year":2024,"kind":"Movie","genre":"Sci-Fi","rating":8.5,"duration":"2h 46m","poster":"https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg","overview":"Paul Atreides joins the Fremen on a path of revenge.","tags":"space epic adventure"},
    {"title":"Oppenheimer","year":2023,"kind":"Movie","genre":"Drama","rating":8.3,"duration":"3h 00m","poster":"https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJIt8st5dglvd.jpg","overview":"The story of the scientist behind the atomic bomb.","tags":"history biography science"},
    {"title":"Spider-Man: No Way Home","year":2021,"kind":"Movie","genre":"Action","rating":8.2,"duration":"2h 28m","poster":"https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg","overview":"Peter Parker faces the consequences of a multiverse spell.","tags":"superhero adventure"},
    {"title":"Avengers: Endgame","year":2019,"kind":"Movie","genre":"Action","rating":8.4,"duration":"3h 01m","poster":"https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg","overview":"The Avengers attempt to reverse a universe-changing disaster.","tags":"superhero sci-fi adventure"},
    {"title":"Joker","year":2019,"kind":"Movie","genre":"Drama","rating":8.4,"duration":"2h 02m","poster":"https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg","overview":"A struggling comedian experiences a disturbing transformation.","tags":"psychological crime dark"},
    {"title":"John Wick","year":2014,"kind":"Movie","genre":"Action","rating":7.4,"duration":"1h 41m","poster":"https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg","overview":"A retired assassin returns to the criminal underworld.","tags":"assassin revenge thriller"},
    {"title":"Top Gun: Maverick","year":2022,"kind":"Movie","genre":"Action","rating":8.2,"duration":"2h 10m","poster":"https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg","overview":"A veteran pilot trains young aviators for a dangerous mission.","tags":"aviation military adventure"},
    {"title":"The Avengers","year":2012,"kind":"Movie","genre":"Action","rating":8.0,"duration":"2h 23m","poster":"https://image.tmdb.org/t/p/w500/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg","overview":"Earth's heroes unite to stop an alien invasion.","tags":"superhero sci-fi"},
    {"title":"Iron Man","year":2008,"kind":"Movie","genre":"Action","rating":7.9,"duration":"2h 06m","poster":"https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9COBYI0dWDJa.jpg","overview":"An engineer builds a powerful suit and becomes a hero.","tags":"superhero technology"},
    {"title":"Black Panther","year":2018,"kind":"Movie","genre":"Action","rating":7.3,"duration":"2h 14m","poster":"https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8wjKA.jpg","overview":"T'Challa defends Wakanda and its future.","tags":"superhero kingdom"},
    {"title":"Doctor Strange","year":2016,"kind":"Movie","genre":"Fantasy","rating":7.5,"duration":"1h 55m","poster":"https://image.tmdb.org/t/p/w500/uGBVj3bEbCoZbDjjl9wTx4g1TQ5.jpg","overview":"A surgeon discovers the mystic arts.","tags":"magic superhero"},
    {"title":"The Shawshank Redemption","year":1994,"kind":"Movie","genre":"Drama","rating":9.3,"duration":"2h 22m","poster":"https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg","overview":"Two prisoners build a lasting friendship and hope for freedom.","tags":"prison hope friendship"},
    {"title":"The Matrix","year":1999,"kind":"Movie","genre":"Sci-Fi","rating":8.7,"duration":"2h 16m","poster":"https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg","overview":"A hacker discovers that reality is a simulation.","tags":"cyberpunk action technology"},
    {"title":"Get Out","year":2017,"kind":"Movie","genre":"Horror","rating":7.8,"duration":"1h 44m","poster":"https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg","overview":"A family visit becomes a frightening mystery.","tags":"psychological suspense thriller"},
    {"title":"La La Land","year":2016,"kind":"Movie","genre":"Romance","rating":8.0,"duration":"2h 08m","poster":"https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg","overview":"A musician and actor pursue their dreams in Los Angeles.","tags":"music musical love"},
    {"title":"Parasite","year":2019,"kind":"Movie","genre":"Thriller","rating":8.5,"duration":"2h 12m","poster":"https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg","overview":"A poor family becomes involved with a wealthy household.","tags":"social suspense dark comedy"},
    {"title":"Arrival","year":2016,"kind":"Movie","genre":"Sci-Fi","rating":7.9,"duration":"1h 56m","poster":"https://image.tmdb.org/t/p/w500/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg","overview":"A linguist tries to communicate with visitors from space.","tags":"aliens language emotional"},
    {"title":"The Grand Budapest Hotel","year":2014,"kind":"Movie","genre":"Comedy","rating":8.1,"duration":"1h 39m","poster":"https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg","overview":"A concierge and his lobby boy investigate a stolen painting.","tags":"quirky adventure comedy"},
    {"title":"Breaking Bad","year":2008,"kind":"TV Series","genre":"Crime","rating":9.5,"duration":"5 Seasons","poster":"https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg","overview":"A chemistry teacher enters the drug trade.","tags":"crime character drama"},
    {"title":"Stranger Things","year":2016,"kind":"TV Series","genre":"Sci-Fi","rating":8.7,"duration":"4 Seasons","poster":"https://image.tmdb.org/t/p/w500/x2LSRK2Cm7MZhjluni1msVJ3wDF.jpg","overview":"Friends discover supernatural mysteries in their town.","tags":"supernatural friendship mystery"},
    {"title":"Money Heist","year":2017,"kind":"TV Series","genre":"Thriller","rating":8.2,"duration":"5 Parts","poster":"https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg","overview":"A mastermind plans elaborate heists with a skilled crew.","tags":"heist crime suspense"},
    {"title":"The Witcher","year":2019,"kind":"TV Series","genre":"Fantasy","rating":8.0,"duration":"3 Seasons","poster":"https://image.tmdb.org/t/p/w500/7vjaCdMw15FEbXyLQTVa04URsPm.jpg","overview":"A monster hunter navigates a world of magic and intrigue.","tags":"monsters magic adventure"},
    {"title":"Game of Thrones","year":2011,"kind":"TV Series","genre":"Fantasy","rating":9.2,"duration":"8 Seasons","poster":"https://image.tmdb.org/t/p/w500/1XS1oqL89opfnbLl8WnZY1O1uJx.jpg","overview":"Noble families battle for power in a fantasy kingdom.","tags":"dragons epic kingdom"},
    {"title":"Wednesday","year":2022,"kind":"TV Series","genre":"Mystery","rating":8.1,"duration":"2 Seasons","poster":"https://image.tmdb.org/t/p/w500/9PFonBhy4cQy7Jz20NpMygczOkv.jpg","overview":"Wednesday Addams investigates strange events at school.","tags":"dark comedy supernatural"},
    {"title":"Squid Game","year":2021,"kind":"TV Series","genre":"Thriller","rating":8.0,"duration":"2 Seasons","poster":"https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg","overview":"Contestants enter deadly games for a life-changing prize.","tags":"survival suspense"},
    {"title":"Peaky Blinders","year":2013,"kind":"TV Series","genre":"Crime","rating":8.7,"duration":"6 Seasons","poster":"https://image.tmdb.org/t/p/w500/vUUqzWa2LnHIVqkaKVlVGkVcZIW.jpg","overview":"A Birmingham gang expands its influence in post-war Britain.","tags":"gangster historical crime"},
    {"title":"The Boys","year":2019,"kind":"TV Series","genre":"Action","rating":8.7,"duration":"4 Seasons","poster":"https://image.tmdb.org/t/p/w500/stTEycfG9928HYGEISBFaG1ngjM.jpg","overview":"Vigilantes confront superheroes who abuse their power.","tags":"superhero satire dark"},
    {"title":"The Last of Us","year":2023,"kind":"TV Series","genre":"Drama","rating":8.7,"duration":"1 Season","poster":"https://image.tmdb.org/t/p/w500/uKvVjHNqB5VmOrdxqAt2F7J78ED.jpg","overview":"A survivor escorts a teenager across a dangerous world.","tags":"survival emotional adventure"},
    {"title":"Sherlock","year":2010,"kind":"TV Series","genre":"Mystery","rating":9.1,"duration":"4 Seasons","poster":"https://image.tmdb.org/t/p/w500/7WTsnHkbA0FaG6R9twfFde0I9hl.jpg","overview":"A brilliant detective solves complex crimes in London.","tags":"detective crime mystery"},
    {"title":"The Office","year":2005,"kind":"TV Series","genre":"Comedy","rating":9.0,"duration":"9 Seasons","poster":"https://image.tmdb.org/t/p/w500/qWnJzyzhwVFP7yQXfR3I3xg4y0H.jpg","overview":"A mockumentary follows the daily lives of office employees.","tags":"workplace comedy"},
    {"title":"Dark","year":2017,"kind":"TV Series","genre":"Sci-Fi","rating":8.7,"duration":"3 Seasons","poster":"https://image.tmdb.org/t/p/w500/apbrbWs8M9lyOpJYU5WXrpFbk1Z.jpg","overview":"A missing child exposes secrets connecting four families.","tags":"time travel mystery"},
    {"title":"Panchayat","year":2020,"kind":"TV Series","genre":"Comedy","rating":8.9,"duration":"3 Seasons","poster":"https://image.tmdb.org/t/p/w500/sgxHe7kZ7nJQ2Y5v8J3v8w4j7kA.jpg","overview":"An engineering graduate adjusts to life as a village secretary.","tags":"Indian village slice of life"},
    {"title":"Kota Factory","year":2019,"kind":"TV Series","genre":"Drama","rating":9.0,"duration":"3 Seasons","poster":"https://image.tmdb.org/t/p/w500/9W7u7d8V3m0M7p5k3f6j1b1g9nR.jpg","overview":"Students prepare for competitive exams while navigating friendships and pressure.","tags":"Indian education students"}
]

# ---------------- SESSION STATE ----------------
if "my_list" not in st.session_state:
    st.session_state.my_list = []

if "selected_title" not in st.session_state:
    st.session_state.selected_title = None

# ---------------- HELPER FUNCTIONS ----------------
def render_cards(data, key_prefix, columns=6):
    """Display movie cards. Defined globally so all filters can use it."""
    if not data:
        st.info("No titles found. Try another genre or search term.")
        return

    cols = st.columns(columns)

    for index, movie in enumerate(data):
        with cols[index % columns]:
            st.image(movie["poster"], use_container_width=True)

            st.markdown(
                f"<div class='movie-title'>{movie['title']}</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<div class='movie-meta'>★ {movie['rating']:.1f} · "
                f"{movie['year']} · {movie['kind']}</div>",
                unsafe_allow_html=True
            )

            left, right = st.columns(2)

            with left:
                if st.button(
                    "Details",
                    key=f"{key_prefix}_details_{movie['title']}",
                    use_container_width=True
                ):
                    st.session_state.selected_title = movie["title"]

            with right:
                saved = movie["title"] in st.session_state.my_list
                label = "✓ Saved" if saved else "+ My List"

                if st.button(
                    label,
                    key=f"{key_prefix}_save_{movie['title']}",
                    use_container_width=True
                ):
                    if saved:
                        st.session_state.my_list.remove(movie["title"])
                    else:
                        st.session_state.my_list.append(movie["title"])

                    st.rerun()


def section_title(title, subtitle=None):
    st.markdown(
        f"<div class='section-title'>{title}</div>",
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f"<div class='section-sub'>{subtitle}</div>",
            unsafe_allow_html=True
        )


def recommendation_score(seed, candidate):
    """Calculate simple content similarity from genre and keywords."""
    if seed["title"] == candidate["title"]:
        return -1

    first = f"{seed['genre']} {seed['tags']}".lower()
    second = f"{candidate['genre']} {candidate['tags']}".lower()

    score = SequenceMatcher(None, first, second).ratio()

    if seed["genre"] == candidate["genre"]:
        score += 0.25

    return score


# ---------------- HEADER ----------------
left, right = st.columns([2, 1])

with left:
    st.markdown(
        "<div class='brand'><span>CINE</span>FLIX</div>"
        "<div class='tagline'>Your next obsession</div>",
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        f"<div style='text-align:right;color:#aaa;padding-top:1rem'>"
        f"Discover your next watch · <b>{len(MOVIES)} titles</b></div>",
        unsafe_allow_html=True
    )

# ---------------- HERO BANNER ----------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">✦ TONIGHT'S FEATURE</div>
    <h1>THE BATMAN</h1>
    <span class="pill">2022</span>
    <span class="pill">★ 7.8</span>
    <span class="pill">Action · Crime · Mystery</span>
    <p>
        Unmask Gotham's darkest secrets. Dive into a cinematic world
        of mystery, danger, and unforgettable stories — handpicked
        for your next watch.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
section = st.radio(
    "Browse",
    ["Home", "Movies", "TV Series", "Top Rated", "Trending", "My List"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------------- FILTERS ----------------
control1, control2, control3 = st.columns([1, 1, 1.5])

genres = ["All genres"] + sorted({m["genre"] for m in MOVIES})

with control1:
    genre_filter = st.selectbox("Genre", genres)

with control2:
    sort_by = st.selectbox(
        "Sort by",
        ["Recommended", "Rating: high to low", "Newest first", "A–Z"]
    )

with control3:
    search = st.text_input(
        "Search",
        placeholder="Search movies, series, genres..."
    )

# ---------------- FILTER LOGIC ----------------
items = MOVIES[:]

if section == "Movies":
    items = [m for m in items if m["kind"] == "Movie"]

elif section == "TV Series":
    items = [m for m in items if m["kind"] == "TV Series"]

elif section == "Top Rated":
    items = [m for m in items if m["rating"] >= 8.5]

elif section == "Trending":
    items = sorted(
        items,
        key=lambda m: (m["year"], m["rating"]),
        reverse=True
    )

elif section == "My List":
    items = [
        m for m in items
        if m["title"] in st.session_state.my_list
    ]

if genre_filter != "All genres":
    items = [m for m in items if m["genre"] == genre_filter]

if search.strip():
    query = search.lower().strip()

    items = [
        m for m in items
        if query in m["title"].lower()
        or query in m["genre"].lower()
        or query in m["tags"].lower()
        or query in m["overview"].lower()
    ]

if sort_by == "Rating: high to low":
    items = sorted(items, key=lambda m: m["rating"], reverse=True)

elif sort_by == "Newest first":
    items = sorted(items, key=lambda m: m["year"], reverse=True)

elif sort_by == "A–Z":
    items = sorted(items, key=lambda m: m["title"].lower())

# ---------------- MOVIE DETAILS ----------------
selected = st.session_state.selected_title

if selected:
    movie = next(
        (m for m in MOVIES if m["title"] == selected),
        None
    )

    if movie:
        with st.container(border=True):
            detail_left, detail_right = st.columns([1, 3])

            with detail_left:
                st.image(movie["poster"], use_container_width=True)

            with detail_right:
                st.markdown(
                    f"<div class='hero-kicker'>SELECTED TITLE</div>"
                    f"<h2>{movie['title']}</h2>",
                    unsafe_allow_html=True
                )

                st.write(
                    f"{movie['year']} · {movie['kind']} · "
                    f"{movie['genre']} · ⭐ {movie['rating']:.1f} · "
                    f"{movie['duration']}"
                )

                st.write(movie["overview"])

                if st.button("Close Details", key="close_details"):
                    st.session_state.selected_title = None
                    st.rerun()

# ---------------- HOME SECTIONS ----------------
if section == "Home" and not search.strip() and genre_filter == "All genres":

    seed = next(m for m in MOVIES if m["title"] == "The Batman")

    recs = sorted(
        MOVIES,
        key=lambda m: recommendation_score(seed, m),
        reverse=True
    )[:8]

    section_title(
        "✦ Recommended For You",
        "Suggestions based on genres and keywords"
    )
    render_cards(recs, "recommended")

    st.markdown("---")

    trending = sorted(
        MOVIES,
        key=lambda m: (m["year"], m["rating"]),
        reverse=True
    )[:8]

    section_title("🔥 Trending Now")
    render_cards(trending, "trending")

    st.markdown("---")

    top_rated = sorted(
        MOVIES,
        key=lambda m: m["rating"],
        reverse=True
    )[:8]

    section_title("⭐ Top Rated")
    render_cards(top_rated, "toprated")

    st.markdown("---")

    section_title("🎬 Browse All Titles", f"{len(MOVIES)} movies and series")
    render_cards(items, "all")

else:
    section_title("Browse Titles", f"{len(items)} title(s) found")
    render_cards(items, "filtered")

# ---------------- MY LIST ----------------
st.markdown("---")

with st.expander(f"♡ My List ({len(st.session_state.my_list)})"):

    saved_items = [
        m for m in MOVIES
        if m["title"] in st.session_state.my_list
    ]

    if saved_items:
        render_cards(saved_items, "mylist")
    else:
        st.caption(
            "Your list is empty. Click + My List on a movie to save it."
        )

# ---------------- SIMILAR TITLES ----------------
selected = st.session_state.selected_title

if selected:
    seed = next(
        (m for m in MOVIES if m["title"] == selected),
        None
    )

    if seed:
        similar = sorted(
            MOVIES,
            key=lambda m: recommendation_score(seed, m),
            reverse=True
        )[:6]

        st.markdown("---")
        section_title(f"Because You Viewed {selected}")
        render_cards(similar, f"similar_{selected}")

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style="text-align:center;color:#777;padding:1.5rem;font-size:.8rem">
    CINEFLIX · Python Movie Recommendation System · Student Project
    <br>
    This application is for movie discovery and does not stream movies.
</div>
""", unsafe_allow_html=True)
