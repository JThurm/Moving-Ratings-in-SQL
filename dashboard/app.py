import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MovieLens Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME
# ============================================================

BG = "#0A0A0C"
PANEL = "#1E1F25"
BORDER = "#3B3F4A"
ACCENT = "#FFB000"
TEXT = "#F2F5F8"
MUTED = "#9BA1AE"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BG};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {PANEL};
        border-right: 1px solid {BORDER};
    }}

    h1 {{
        font-size: 2.7rem !important;
        font-weight: 650 !important;
        letter-spacing: -0.045em;
        color: {TEXT};
        margin-bottom: 0.2rem !important;
    }}

    h2 {{
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.025em;
        color: {TEXT};
        margin-top: 2rem !important;
    }}

    h3 {{
        color: {TEXT};
        font-weight: 600 !important;
    }}

    p {{
        color: {MUTED};
    }}

    div[data-testid="stMetric"] {{
        background-color: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT};
        font-weight: 600;
    }}

    button[data-baseweb="tab"] {{
        color: {MUTED};
        font-size: 0.95rem;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {ACCENT};
    }}

    div[data-baseweb="tab-highlight"] {{
        background-color: {ACCENT};
    }}

    div[data-baseweb="select"] > div {{
        background-color: {PANEL};
        border-color: {BORDER};
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 8px;
        overflow: hidden;
    }}

    div[data-testid="stAlert"] {{
        background-color: {PANEL};
        border: 1px solid {BORDER};
    }}

    hr {{
        border-color: {BORDER};
    }}

    .section-description {{
        color: {MUTED};
        font-size: 0.92rem;
        max-width: 850px;
        margin-top: -0.5rem;
        margin-bottom: 1.2rem;
        line-height: 1.6;
    }}

    .finding-card {{
        background-color: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin: 0.8rem 0 1.4rem 0;
    }}

    .finding-number {{
        color: {ACCENT};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }}

    .finding-title {{
        color: {TEXT};
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.45rem;
    }}

    .finding-text {{
        color: {MUTED};
        font-size: 0.92rem;
        line-height: 1.65;
    }}

    .takeaway {{
        border-left: 3px solid {ACCENT};
        padding: 0.7rem 1rem;
        margin: 1rem 0 1.5rem 0;
        background-color: rgba(255, 176, 0, 0.04);
    }}

    .takeaway-title {{
        color: {ACCENT};
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.25rem;
    }}

    .takeaway-text {{
        color: {TEXT};
        font-size: 0.9rem;
        line-height: 1.55;
    }}

    .footer {{
        color: {MUTED};
        font-size: 0.78rem;
        text-align: center;
        padding-top: 2rem;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"


# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_csv(filename):

    path = RESULTS_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path, encoding="utf-8")

    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp1252")


# ============================================================
# LOAD DATA
# ============================================================

year = load_csv("01_rating_trends_by_year.csv")
genre_year = load_csv("02_genre_popularity_by_year.csv")
yoy = load_csv("03_genre_yoy_change.csv")
top_genre = load_csv("04_top_genre_per_year.csv")
polarizing = load_csv("05_polarizing_movies.csv")
seasonal = load_csv("06_seasonal_patterns.csv")

era = load_csv("07_historical_era_genres.csv")
genre_stats = load_csv("08_genre_popularity_vs_rating.csv")
disagreement = load_csv("09_rating_disagreement_over_time.csv")
polarization = load_csv("10_genre_polarization.csv")
volume_variability = load_csv("11_rating_volume_vs_variability.csv")
events = load_csv("12_historical_events.csv")


# ============================================================
# PLOTLY THEME
# ============================================================

def style_figure(fig):

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(
            family="Inter, Arial, sans-serif",
            color=TEXT,
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=30,
        ),
        hoverlabel=dict(
            bgcolor=PANEL,
            bordercolor=BORDER,
            font=dict(color=TEXT),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED),
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=BORDER,
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=BORDER,
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    return fig


# ============================================================
# HEADER
# ============================================================

st.title("MovieLens Analytics")

st.markdown(
    """
    <div style="
        color:#9BA1AE;
        font-size:1rem;
        max-width:850px;
        margin-bottom:1.5rem;
    ">
        An interactive exploration of movie ratings, genre popularity,
        audience disagreement, seasonal behavior, and historical context.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## Filters")

if not year.empty:

    min_year = int(year["release_year"].min())
    max_year = int(year["release_year"].max())

    year_range = st.sidebar.slider(
        "Release year",
        min_year,
        max_year,
        (min_year, max_year),
    )

else:

    year_range = (1900, 2018)


st.sidebar.markdown("---")

st.sidebar.caption("Dataset")
st.sidebar.caption("MovieLens ml-latest-small")

st.sidebar.caption("Tools")
st.sidebar.caption("PostgreSQL · Python · Pandas · Plotly")


# ============================================================
# OVERVIEW METRICS
# ============================================================

if not year.empty:

    total_years = year["release_year"].nunique()

    total_ratings = (
        year["rating_count"].sum()
        if "rating_count" in year.columns
        else 0
    )

else:

    total_years = 0
    total_ratings = 0


total_genres = (
    genre_stats["genre"].nunique()
    if not genre_stats.empty
    else 0
)


st.markdown("### Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Release Years", f"{total_years:,}")

with c2:
    st.metric("Rating Records", f"{total_ratings:,}")

with c3:
    st.metric("Genres", f"{total_genres:,}")

with c4:
    st.metric(
        "Selected Range",
        f"{year_range[0]}–{year_range[1]}",
    )


st.markdown("---")


# ============================================================
# MAIN TABS
# ============================================================

overview_tab, findings_tab, explore_tab, methodology_tab = st.tabs(
    [
        "Overview",
        "Findings",
        "Explore Data",
        "Methodology",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with overview_tab:

    st.header("Overview")

    st.markdown(
        """
        <div class="section-description">
        Start here for a high-level view of the dataset. The Findings tab
        summarizes the most important patterns, while Explore Data provides
        access to the detailed analyses.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # AVERAGE RATING
    # --------------------------------------------------------

    if not year.empty:

        y = year[
            year["release_year"].between(*year_range)
        ].copy()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=y["release_year"],
                y=y["average_rating"],
                mode="lines",
                line=dict(
                    color=ACCENT,
                    width=2.5,
                ),
                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>Average rating: %{y:.2f}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="Average Rating by Release Year",
            xaxis_title="Release Year",
            yaxis_title="Average Rating",
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RATING VOLUME
    # --------------------------------------------------------

    if not year.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=y["release_year"],
                y=y["rating_count"],
                mode="lines",
                line=dict(
                    color=ACCENT,
                    width=2,
                ),
                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>Ratings: %{y:,}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="Rating Volume by Release Year",
            xaxis_title="Release Year",
            yaxis_title="Number of Ratings",
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # PROJECT GUIDE
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("How to Use This Dashboard")

    guide1, guide2, guide3 = st.columns(3)

    with guide1:
        st.markdown(
            """
            **01 · Start with Findings**

            See the major conclusions from the analysis without needing to
            interpret every visualization yourself.
            """
        )

    with guide2:
        st.markdown(
            """
            **02 · Explore the Data**

            Dive into individual SQL analyses and interact with the charts
            when you want more detail.
            """
        )

    with guide3:
        st.markdown(
            """
            **03 · Review the Methodology**

            Learn how the MovieLens data was transformed, analyzed, and
            presented.
            """
        )


# ============================================================
# FINDINGS
# ============================================================

with findings_tab:

    st.header("Key Findings")

    st.markdown(
        """
        <div class="section-description">
        A guided summary of the major patterns identified in the MovieLens
        dataset. Each finding is supported by an underlying SQL analysis
        that can be explored in the Explore Data section.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINDING 1
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 01</div>
            <div class="finding-title">
                Popularity does not necessarily mean higher ratings
            </div>
            <div class="finding-text">
                Genres with the largest numbers of ratings are not always the
                genres with the highest average ratings. This separates
                audience attention from audience satisfaction and shows why
                rating volume and rating quality should be analyzed together.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not genre_stats.empty:

        gs = genre_stats[
            ~genre_stats["genre"].isin(
                ["(no genres listed)"]
            )
        ].dropna().copy()

        fig = px.scatter(
            gs,
            x="rating_count",
            y="average_rating",
            text="genre",
            size="rating_count",
            hover_data=[
                c for c in [
                    "popularity_rank",
                    "rating_rank",
                ]
                if c in gs.columns
            ],
        )

        fig.update_traces(
            marker=dict(
                color=ACCENT,
                opacity=0.75,
            ),
            textposition="top center",
            textfont=dict(
                size=10,
                color=TEXT,
            ),
        )

        fig.update_layout(
            title="Genre Popularity vs. Average Rating",
            xaxis_title="Number of Ratings",
            yaxis_title="Average Rating",
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="takeaway">
            <div class="takeaway-title">Takeaway</div>
            <div class="takeaway-text">
                A genre can dominate in rating volume without having the
                highest average rating.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINDING 2
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 02</div>
            <div class="finding-title">
                Rating samples become much larger in later years
            </div>
            <div class="finding-text">
                The number of submitted ratings varies dramatically across
                release years. Early films often have very small samples,
                meaning unusually high or low averages may be driven by only
                a handful of observations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not year.empty:

        y = year[
            year["release_year"].between(*year_range)
        ].copy()

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=y["release_year"],
                y=y["rating_count"],
                mode="lines",
                line=dict(
                    color=ACCENT,
                    width=2.5,
                ),
                hovertemplate=(
                    "<b>%{x}</b>"
                    "<br>Ratings: %{y:,}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title="Rating Volume Across Release Years",
            xaxis_title="Release Year",
            yaxis_title="Number of Ratings",
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="takeaway">
            <div class="takeaway-title">Interpretation</div>
            <div class="takeaway-text">
                Early-year averages should be interpreted cautiously because
                their sample sizes are often much smaller than those of later
                years.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINDING 3
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 03</div>
            <div class="finding-title">
                Some genres produce more disagreement than others
            </div>
            <div class="finding-text">
                Average rating alone does not describe how consistently viewers
                feel about a genre. Rating standard deviation provides another
                perspective by measuring how widely ratings are distributed.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not polarization.empty:

        p = polarization[
            ~polarization["genre"].isin(
                ["(no genres listed)"]
            )
        ].sort_values(
            "rating_stddev",
            ascending=True,
        )

        fig = px.bar(
            p,
            x="rating_stddev",
            y="genre",
            orientation="h",
        )

        fig.update_traces(
            marker_color=ACCENT
        )

        fig.update_layout(
            title="Genre Rating Variability",
            xaxis_title="Rating Standard Deviation",
            yaxis_title=None,
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="takeaway">
            <div class="takeaway-title">Takeaway</div>
            <div class="takeaway-text">
                Higher variability indicates greater disagreement among
                viewers; it does not automatically mean that a genre is
                poorly rated.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINDING 4
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 04</div>
            <div class="finding-title">
                Genre activity changes across historical eras
            </div>
            <div class="finding-text">
                The distribution of rating activity across genres changes
                substantially between historical periods. Comparing eras helps
                identify broader shifts that may not be obvious when looking
                at individual years.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not era.empty:

        e = era[
            era["historical_era"].notna()
        ].copy()

        e = e[
            ~e["genre"].isin(
                ["(no genres listed)"]
            )
        ]

        # Show the most frequently rated genres overall.
        top_era_genres = (
            e.groupby("genre")["rating_count"]
            .sum()
            .nlargest(8)
            .index
        )

        e = e[
            e["genre"].isin(top_era_genres)
        ]

        fig = px.bar(
            e.sort_values("era_order"),
            x="historical_era",
            y="rating_count",
            color="genre",
            barmode="group",
            hover_data=[
                "average_rating"
            ],
        )

        fig.update_layout(
            title="Genre Rating Volume Across Historical Eras",
            xaxis_title="Historical Era",
            yaxis_title="Rating Volume",
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


    # ========================================================
    # FINDING 5
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 05</div>
            <div class="finding-title">
                Some individual movies strongly divide audiences
            </div>
            <div class="finding-text">
                Movies with similar average ratings can have very different
                distributions of individual ratings. Standard deviation makes
                it possible to identify films where viewers disagree more
                strongly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not polarizing.empty:

        pm = polarizing.copy()

        std_columns = [
            c for c in pm.columns
            if "std" in c.lower()
        ]

        if std_columns:

            std_col = std_columns[0]

            pm = (
                pm.sort_values(
                    std_col,
                    ascending=False,
                )
                .head(15)
            )

            fig = px.bar(
                pm.sort_values(
                    std_col,
                    ascending=True,
                ),
                x=std_col,
                y="title",
                orientation="h",
                hover_data=[
                    c for c in [
                        "average_rating",
                        "rating_count",
                    ]
                    if c in pm.columns
                ],
            )

            fig.update_traces(
                marker_color=ACCENT
            )

            fig.update_layout(
                title="Most Polarizing Movies",
                xaxis_title="Rating Standard Deviation",
                yaxis_title=None,
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # ========================================================
    # FINDING 6
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 06</div>
            <div class="finding-title">
                Genre leadership changes over time
            </div>
            <div class="finding-text">
                The genre receiving the most rating activity is not constant
                throughout the dataset. Looking at the top genre for each year
                highlights periods where audience attention shifted between
                different genres.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not top_genre.empty:

        tg = top_genre[
            top_genre["release_year"].between(
                *year_range
            )
        ].copy()

        fig = px.scatter(
            tg,
            x="release_year",
            y="genre",
            hover_data=[
                c for c in [
                    "average_rating",
                    "rating_count",
                    "genre_rank",
                ]
                if c in tg.columns
            ],
        )

        fig.update_traces(
            marker=dict(
                color=ACCENT,
                size=9,
            )
        )

        fig.update_layout(
            title="Top Genre by Year",
            xaxis_title="Release Year",
            yaxis_title="Top Genre",
            showlegend=False,
        )

        style_figure(fig)

        st.plotly_chart(
            fig,
            use_container_width=True,
        )


    # ========================================================
    # FINDING 7
    # ========================================================

    st.markdown(
        """
        <div class="finding-card">
            <div class="finding-number">Finding 07</div>
            <div class="finding-title">
                Seasonal rating activity is uneven, but not necessarily
                predictable
            </div>
            <div class="finding-text">
                Rating activity fluctuates between months, with several
                noticeable spikes. However, these variations do not by
                themselves establish a consistent seasonal effect.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not seasonal.empty:

        s = seasonal.copy()

        month_columns = [
            c for c in s.columns
            if "month" in c.lower()
        ]

        count_columns = [
            c for c in s.columns
            if "count" in c.lower()
        ]

        if month_columns and count_columns:

            month_col = month_columns[0]
            count_col = count_columns[0]

            seasonal_summary = (
                s.groupby(
                    month_col,
                    as_index=False
                )[count_col]
                .sum()
            )

            fig = px.bar(
                seasonal_summary,
                x=month_col,
                y=count_col,
            )

            fig.update_traces(
                marker_color=ACCENT
            )

            fig.update_layout(
                title="Rating Activity by Month",
                xaxis_title="Month",
                yaxis_title="Rating Volume",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


# ============================================================
# EXPLORE DATA
# ============================================================

with explore_tab:

    st.header("Explore the Data")

    st.markdown(
        """
        <div class="section-description">
        Dive into the individual analyses behind the findings. These
        visualizations are intended for exploration rather than presenting a
        single conclusion.
        </div>
        """,
        unsafe_allow_html=True,
    )

    trend_tab, genre_tab, audience_explore_tab, history_explore_tab = st.tabs(
        [
            "Rating Trends",
            "Genres",
            "Audience",
            "Historical Context",
        ]
    )


    # ========================================================
    # RATING TRENDS
    # ========================================================

    with trend_tab:

        st.subheader("Average Rating by Release Year")

        if not year.empty:

            y = year[
                year["release_year"].between(
                    *year_range
                )
            ].copy()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=y["release_year"],
                    y=y["average_rating"],
                    mode="lines",
                    line=dict(
                        color=ACCENT,
                        width=2.5,
                    ),
                )
            )

            fig.update_layout(
                xaxis_title="Release Year",
                yaxis_title="Average Rating",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        st.subheader("Rating Volume by Release Year")

        if not year.empty:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=y["release_year"],
                    y=y["rating_count"],
                    mode="lines",
                    line=dict(
                        color=ACCENT,
                        width=2,
                    ),
                )
            )

            fig.update_layout(
                xaxis_title="Release Year",
                yaxis_title="Number of Ratings",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        st.subheader("Rating Disagreement Over Time")

        if not disagreement.empty:

            d = disagreement[
                disagreement["release_year"].between(
                    *year_range
                )
            ].copy()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=d["release_year"],
                    y=d["rating_stddev"],
                    mode="lines",
                    line=dict(
                        color=ACCENT,
                        width=2.5,
                    ),
                    hovertemplate=(
                        "<b>%{x}</b>"
                        "<br>Std. deviation: %{y:.2f}"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                xaxis_title="Release Year",
                yaxis_title="Rating Standard Deviation",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # ========================================================
    # GENRES
    # ========================================================

    with genre_tab:

        # ----------------------------------------------------
        # GENRE POPULARITY OVER TIME
        # ----------------------------------------------------

        st.subheader("Genre Popularity Over Time")

        if not genre_year.empty:

            gy = genre_year[
                genre_year["release_year"].between(
                    *year_range
                )
            ].copy()

            available_genres = sorted(
                gy[
                    ~gy["genre"].isin(
                        ["(no genres listed)"]
                    )
                ]["genre"]
                .dropna()
                .unique()
            )

            selected_genres = st.multiselect(
                "Select genres",
                available_genres,
                default=available_genres[:5]
                if len(available_genres) >= 5
                else available_genres,
                key="genre_trend_selection",
            )

            if selected_genres:

                selected_data = gy[
                    gy["genre"].isin(
                        selected_genres
                    )
                ]

                fig = px.line(
                    selected_data,
                    x="release_year",
                    y="rating_count",
                    color="genre",
                    markers=False,
                )

                fig.update_layout(
                    title="Rating Volume by Genre",
                    xaxis_title="Release Year",
                    yaxis_title="Number of Ratings",
                )

                style_figure(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

        # ----------------------------------------------------
        # POPULARITY VS RATING
        # ----------------------------------------------------

        st.subheader("Popularity vs. Average Rating")

        if not genre_stats.empty:

            gs = genre_stats[
                ~genre_stats["genre"].isin(
                    ["(no genres listed)"]
                )
            ].dropna().copy()

            fig = px.scatter(
                gs,
                x="rating_count",
                y="average_rating",
                text="genre",
                size="rating_count",
                hover_data=[
                    c for c in [
                        "popularity_rank",
                        "rating_rank",
                    ]
                    if c in gs.columns
                ],
            )

            fig.update_traces(
                marker=dict(
                    color=ACCENT,
                    opacity=0.75,
                ),
                textposition="top center",
                textfont=dict(
                    size=10,
                    color=TEXT,
                ),
            )

            fig.update_layout(
                xaxis_title="Rating Volume",
                yaxis_title="Average Rating",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ----------------------------------------------------
        # HISTORICAL ERA
        # ----------------------------------------------------

        st.subheader(
            "Genre Volume Across Historical Eras"
        )

        if not era.empty:

            e = era[
                ~era["genre"].isin(
                    ["(no genres listed)"]
                )
            ].copy()

            top_era_genres = (
                e.groupby("genre")["rating_count"]
                .sum()
                .nlargest(8)
                .index
            )

            e = e[
                e["genre"].isin(
                    top_era_genres
                )
            ]

            fig = px.bar(
                e.sort_values("era_order"),
                x="historical_era",
                y="rating_count",
                color="genre",
                barmode="group",
            )

            fig.update_layout(
                xaxis_title="Historical Era",
                yaxis_title="Rating Volume",
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ----------------------------------------------------
        # YOY
        # ----------------------------------------------------

        st.subheader(
            "Year-over-Year Genre Change"
        )

        if not yoy.empty:

            genres_available = sorted(
                yoy[
                    ~yoy["genre"].isin(
                        ["(no genres listed)"]
                    )
                ]["genre"]
                .dropna()
                .unique()
            )

            selected_genre = st.selectbox(
                "Genre",
                genres_available,
                key="explore_yoy_genre",
            )

            gy = yoy[
                (yoy["genre"] == selected_genre)
                & (
                    yoy["release_year"].between(
                        *year_range
                    )
                )
            ].copy()

            change_columns = [
                c for c in gy.columns
                if "change" in c.lower()
            ]

            if change_columns:

                change_col = change_columns[0]

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=gy["release_year"],
                        y=gy[change_col],
                        marker_color=ACCENT,
                    )
                )

                fig.update_layout(
                    xaxis_title="Release Year",
                    yaxis_title="Year-over-Year Change",
                    showlegend=False,
                )

                style_figure(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ----------------------------------------------------
        # TOP GENRE
        # ----------------------------------------------------

        st.subheader(
            "Top-Rated Genre by Year"
        )

        if not top_genre.empty:

            tg = top_genre[
                top_genre["release_year"].between(
                    *year_range
                )
            ].copy()

            fig = px.scatter(
                tg,
                x="release_year",
                y="genre",
                hover_data=[
                    c for c in [
                        "average_rating",
                        "rating_count",
                        "genre_rank",
                    ]
                    if c in tg.columns
                ],
            )

            fig.update_traces(
                marker=dict(
                    color=ACCENT,
                    size=9,
                )
            )

            fig.update_layout(
                xaxis_title="Release Year",
                yaxis_title="Top Genre",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ----------------------------------------------------
        # GENRE POLARIZATION
        # ----------------------------------------------------

        st.subheader(
            "Genre Polarization"
        )

        if not polarization.empty:

            p = polarization[
                ~polarization["genre"].isin(
                    ["(no genres listed)"]
                )
            ].sort_values(
                "rating_stddev",
                ascending=True,
            )

            fig = px.bar(
                p,
                x="rating_stddev",
                y="genre",
                orientation="h",
            )

            fig.update_traces(
                marker_color=ACCENT
            )

            fig.update_layout(
                xaxis_title="Rating Standard Deviation",
                yaxis_title=None,
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # ========================================================
    # AUDIENCE
    # ========================================================

    with audience_explore_tab:

        # ----------------------------------------------------
        # POLARIZING MOVIES
        # ----------------------------------------------------

        st.subheader("Most Polarizing Movies")

        if not polarizing.empty:

            pm = polarizing.copy()

            std_columns = [
                c for c in pm.columns
                if "std" in c.lower()
            ]

            if std_columns:

                std_col = std_columns[0]

                pm = pm.sort_values(
                    std_col,
                    ascending=False,
                ).head(20)

                fig = px.bar(
                    pm.sort_values(
                        std_col,
                        ascending=True,
                    ),
                    x=std_col,
                    y="title",
                    orientation="h",
                    hover_data=[
                        c for c in [
                            "average_rating",
                            "rating_count",
                        ]
                        if c in pm.columns
                    ],
                )

                fig.update_traces(
                    marker_color=ACCENT
                )

                fig.update_layout(
                    xaxis_title="Rating Standard Deviation",
                    yaxis_title=None,
                    showlegend=False,
                )

                style_figure(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ----------------------------------------------------
        # VOLUME VS VARIABILITY
        # ----------------------------------------------------

        st.subheader(
            "Rating Volume vs. Variability"
        )

        if not volume_variability.empty:

            vv = volume_variability.dropna(
                subset=[
                    "rating_count",
                    "rating_stddev",
                ]
            ).copy()

            fig = px.scatter(
                vv,
                x="rating_count",
                y="rating_stddev",
                hover_data=[
                    c for c in [
                        "title",
                        "release_year",
                        "average_rating",
                    ]
                    if c in vv.columns
                ],
            )

            fig.update_traces(
                marker=dict(
                    color=ACCENT,
                    size=7,
                    opacity=0.55,
                )
            )

            fig.update_xaxes(
                type="log"
            )

            fig.update_layout(
                xaxis_title="Number of Ratings",
                yaxis_title="Rating Standard Deviation",
                showlegend=False,
            )

            style_figure(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            if len(vv):

                row = vv.iloc[0]

                a, b, c = st.columns(3)

                with a:
                    st.metric(
                        "Volume ↔ Variability",
                        f"{row['volume_vs_variability']:.3f}",
                    )

                with b:
                    st.metric(
                        "Volume ↔ Average Rating",
                        f"{row['volume_vs_average']:.3f}",
                    )

                with c:
                    st.metric(
                        "Average ↔ Variability",
                        f"{row['average_vs_variability']:.3f}",
                    )


        # ----------------------------------------------------
        # SEASONAL
        # ----------------------------------------------------

        st.subheader(
            "Seasonal Rating Activity"
        )

        if not seasonal.empty:

            s = seasonal.copy()

            month_columns = [
                c for c in s.columns
                if "month" in c.lower()
            ]

            count_columns = [
                c for c in s.columns
                if "count" in c.lower()
            ]

            if month_columns and count_columns:

                month_col = month_columns[0]
                count_col = count_columns[0]

                seasonal_summary = (
                    s.groupby(
                        month_col,
                        as_index=False
                    )[count_col]
                    .sum()
                )

                fig = px.bar(
                    seasonal_summary,
                    x=month_col,
                    y=count_col,
                )

                fig.update_traces(
                    marker_color=ACCENT
                )

                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Rating Volume",
                    showlegend=False,
                )

                style_figure(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


    # ========================================================
    # HISTORICAL CONTEXT
    # ========================================================

    with history_explore_tab:

        st.subheader(
            "Historical & Industry Events"
        )

        st.markdown(
            """
            <div class="section-description">
            These comparisons place rating and genre patterns alongside
            selected historical and industry events. They should be interpreted
            as contextual comparisons rather than evidence of causation.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not events.empty:

            ev = events[
                events["release_year"].between(
                    *year_range
                )
            ].copy()

            if not ev.empty:

                selected_event = st.selectbox(
                    "Select an event",
                    sorted(
                        ev["event_name"]
                        .dropna()
                        .unique()
                    ),
                    key="historical_event",
                )

                event_data = ev[
                    ev["event_name"] == selected_event
                ]

                fig = px.bar(
                    event_data.sort_values(
                        "rating_count",
                        ascending=True,
                    ),
                    x="rating_count",
                    y="genre",
                    orientation="h",
                    hover_data=[
                        c for c in [
                            "release_year",
                            "average_rating",
                            "rating_stddev",
                        ]
                        if c in event_data.columns
                    ],
                )

                fig.update_traces(
                    marker_color=ACCENT
                )

                fig.update_layout(
                    xaxis_title="Rating Volume",
                    yaxis_title=None,
                    showlegend=False,
                )

                style_figure(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                st.subheader("Event Data")

                display_columns = [
                    "release_year",
                    "event_name",
                    "event_type",
                    "genre",
                    "rating_count",
                    "average_rating",
                    "rating_stddev",
                ]

                available_columns = [
                    c
                    for c in display_columns
                    if c in event_data.columns
                ]

                st.dataframe(
                    event_data[
                        available_columns
                    ].sort_values(
                        [
                            "release_year",
                            "rating_count",
                        ],
                        ascending=[
                            True,
                            False,
                        ],
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

            else:

                st.info(
                    "No event data is available "
                    "for the selected year range."
                )


# ============================================================
# METHODOLOGY
# ============================================================

with methodology_tab:

    st.header("Methodology")

    st.markdown(
        """
        <div class="section-description">
        How the MovieLens data was transformed, analyzed, and presented in
        this project.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader("Data Pipeline")

    st.code(
        """
MovieLens Dataset
        │
        ▼
PostgreSQL Database
        │
        ├── movies
        ├── ratings
        └── movie_genres
        │
        ▼
SQL Analysis Queries
        │
        ▼
CSV Results
        │
        ▼
Python + Pandas
        │
        ▼
Streamlit + Plotly Dashboard
        """,
        language="text",
    )


    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    st.subheader("Database Design")

    st.markdown(
        """
        The MovieLens dataset stores movie genres in a delimited field.
        For analysis, genres were normalized into a separate
        `movie_genres` table containing one row per movie-genre relationship.

        This structure allows genres to be independently grouped, filtered,
        compared, and analyzed using SQL.
        """
    )


    # --------------------------------------------------------
    # ANALYSES
    # --------------------------------------------------------

    st.subheader("Analyses Included")

    analysis_data = pd.DataFrame(
        {
            "Analysis": [
                "Rating trends",
                "Genre popularity",
                "Year-over-year genre change",
                "Top genre by year",
                "Movie polarization",
                "Seasonal patterns",
                "Historical-era genre trends",
                "Popularity vs. rating",
                "Rating disagreement over time",
                "Genre polarization",
                "Rating volume vs. variability",
                "Historical event comparisons",
            ],
            "Result": [
                "01_rating_trends_by_year.csv",
                "02_genre_popularity_by_year.csv",
                "03_genre_yoy_change.csv",
                "04_top_genre_per_year.csv",
                "05_polarizing_movies.csv",
                "06_seasonal_patterns.csv",
                "07_historical_era_genres.csv",
                "08_genre_popularity_vs_rating.csv",
                "09_rating_disagreement_over_time.csv",
                "10_genre_polarization.csv",
                "11_rating_volume_vs_variability.csv",
                "12_historical_events.csv",
            ],
        }
    )

    st.dataframe(
        analysis_data,
        use_container_width=True,
        hide_index=True,
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    st.subheader("Key Metrics")

    m1, m2 = st.columns(2)

    with m1:

        st.markdown(
            """
            **Average Rating**

            The arithmetic mean of ratings associated with a movie, genre,
            or release year.

            **Rating Volume**

            The number of submitted ratings included in an analysis.

            **Genre Popularity**

            Measured using rating volume rather than movie production count.
            """
        )

    with m2:

        st.markdown(
            """
            **Rating Variability**

            Measured using standard deviation. Higher values indicate
            greater disagreement between viewers.

            **Polarization**

            Higher rating standard deviation is used as an indicator of
            greater audience disagreement.

            **Correlation**

            Pearson correlation coefficients are used to explore linear
            relationships between rating volume, average rating, and
            variability.
            """
        )


    # --------------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------------

    st.subheader("Important Limitations")

    st.markdown(
        """
        - Rating volume represents submitted ratings, not unique viewers.
        - Older movies generally have smaller rating samples.
        - Small samples can make average ratings less reliable.
        - MovieLens users are not necessarily representative of all moviegoers.
        - A high average rating does not necessarily indicate audience agreement.
        - Genre popularity refers to rating activity rather than total movies
          produced.
        - Historical events provide contextual comparisons rather than proof
          of causation.
        - Missing genres are represented by `(no genres listed)` and are
          excluded from several genre-specific analyses.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        MovieLens Analytics · PostgreSQL · Python · Pandas · Plotly
        <br><br>
        Rating volume represents submitted ratings, not unique viewers
        or movie production volume. Historical events represent contextual
        correlations rather than proof of causation.
    </div>
    """,
    unsafe_allow_html=True,
)