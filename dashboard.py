import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="IPL Cricket Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ==========================================
# 2. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #101820;
    color: white;
}

h1, h2, h3 {
    color: #FEE715;
}

div[data-testid="stMetric"] {
    background-color: #243447;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #FEE715;
}

div[data-testid="stMetricValue"] {
    color: #FEE715;
}

section[data-testid="stSidebar"] {
    background-color: #243447;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    deliveries = pd.read_csv("dataset/cleaned_deliveries.csv")
    matches = pd.read_csv("dataset/cleaned_matches.csv")
    return deliveries, matches

df, matches = load_data()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🏏 IPL Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Player Analysis",
        "Bowler Analysis",
        "Team Analysis",
        "Match Winner Analysis"
    ]
)

st.sidebar.divider()

# ==========================================
# 5. SEASON FILTER
# ==========================================

seasons = sorted(
    matches["season"].dropna().unique(),
    key=str
)

selected_season = st.sidebar.selectbox(
    "Select IPL Season",
    ["All Seasons"] + list(seasons)
)

if selected_season == "All Seasons":
    season_matches = matches.copy()
    season_df = df.copy()
else:
    season_matches = matches[
        matches["season"] == selected_season
    ]

    season_df = df[
        df["match_id"].isin(season_matches["id"])
    ]

# ==========================================
# 6. DASHBOARD TITLE
# ==========================================

st.title("🏏 IPL Cricket Performance Dashboard")

st.write(
    "Explore IPL statistics, player performance "
    "and team records."
)

st.divider()

# ==========================================
# 7. OVERVIEW PAGE
# ==========================================

if page == "Overview":

    st.header("📊 IPL Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Matches",
            season_matches["id"].nunique()
        )

    with col2:
        st.metric(
            "Total Deliveries",
            len(season_df)
        )

    with col3:
        st.metric(
            "Total Runs",
            int(season_df["total_runs"].sum())
        )

    st.divider()

    st.subheader("🏆 Top 10 Run Scorers")

    player_runs = (
        season_df.groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    if not player_runs.empty:

        fig, ax = plt.subplots(figsize=(10, 5))

        player_runs.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_xlabel("Total Runs")
        ax.set_ylabel("Players")

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    st.subheader("🏏 Team Performance")

    team_runs = (
        season_df.groupby("batting_team")["total_runs"]
        .sum()
        .sort_values(ascending=False)
    )

    if not team_runs.empty:

        fig2, ax2 = plt.subplots(figsize=(12, 5))

        team_runs.plot(kind="bar", ax=ax2)

        ax2.set_xlabel("Teams")
        ax2.set_ylabel("Total Runs")

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig2)
        plt.close(fig2)

# ==========================================
# 8. PLAYER ANALYSIS PAGE
# ==========================================

elif page == "Player Analysis":

    st.header("👤 Player Performance Analysis")

    players = sorted(
        season_df["batter"].dropna().unique()
    )

    if players:

        selected_player = st.selectbox(
            "Select Player",
            players
        )

        player_data = season_df[
            season_df["batter"] == selected_player
        ]

        total_runs = player_data["batsman_runs"].sum()

        balls_faced = player_data[
            player_data["extras_type"].fillna("").str.lower() != "wides"
        ].shape[0]

        strike_rate = (
            total_runs / balls_faced * 100
            if balls_faced > 0 else 0
        )

        col1, col2 = st.columns(2)

        col1.metric("Total Runs", int(total_runs))
        col2.metric("Strike Rate", round(strike_rate, 2))

        st.subheader("Player Run Distribution")

        runs_per_match = (
            player_data.groupby("match_id")["batsman_runs"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        runs_per_match.plot(
            kind="line",
            marker="o",
            ax=ax
        )

        ax.set_xlabel("Match ID")
        ax.set_ylabel("Runs")
        ax.set_title("Runs Scored in Each Match")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No player data available.")

# ==========================================
# 9. BOWLER ANALYSIS PAGE
# ==========================================

elif page == "Bowler Analysis":

    st.header("🎯 Bowler Performance Analysis")

    wickets = season_df[
        (season_df["is_wicket"] == 1) &
        (~season_df["dismissal_kind"].isin([
            "run out",
            "retired hurt",
            "obstructing the field"
        ]))
    ]

    bowler_wickets = (
        wickets.groupby("bowler")["is_wicket"]
        .sum()
        .sort_values(ascending=False)
    )

    if not bowler_wickets.empty:

        selected_bowler = st.selectbox(
            "Select Bowler",
            sorted(bowler_wickets.index)
        )

        total_wickets = bowler_wickets[selected_bowler]

        st.metric("Total Wickets", int(total_wickets))

        st.subheader("Top 10 Wicket-Taking Bowlers")

        top_bowlers = bowler_wickets.head(10)

        fig, ax = plt.subplots(figsize=(10, 5))

        top_bowlers.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_xlabel("Total Wickets")
        ax.set_ylabel("Bowlers")

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No bowling data available.")

# ==========================================
# 10. TEAM ANALYSIS PAGE
# ==========================================

elif page == "Team Analysis":

    st.header("🏏 Team Performance Analysis")

    teams = sorted(
        season_df["batting_team"].dropna().unique()
    )

    if teams:

        selected_team = st.selectbox(
            "Select IPL Team",
            teams
        )

        team_data = season_df[
            season_df["batting_team"] == selected_team
        ]

        team_matches = season_matches[
            (season_matches["team1"] == selected_team) |
            (season_matches["team2"] == selected_team)
        ]

        total_runs = team_data["total_runs"].sum()

        total_matches = team_matches["id"].nunique()

        total_wins = (
            team_matches["winner"] == selected_team
        ).sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Runs", int(total_runs))
        col2.metric("Matches Played", int(total_matches))
        col3.metric("Matches Won", int(total_wins))

        st.subheader("Team Run Distribution")

        runs_by_match = (
            team_data.groupby("match_id")["total_runs"]
            .sum()
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        runs_by_match.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Match ID")
        ax.set_ylabel("Runs")
        ax.set_title("Team Runs in Each Match")

        plt.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    else:
        st.info("No team data available.")

# ==========================================
# 11. MATCH WINNER ANALYSIS PAGE
# ==========================================

elif page == "Match Winner Analysis":

    st.header("🥇 IPL Match Winner Analysis")

    winner_data = season_matches[
        season_matches["winner"].notna()
    ]

    winner_counts = (
        winner_data["winner"]
        .value_counts()
        .head(10)
    )

    if not winner_counts.empty:

        st.subheader("Top 10 Teams by Matches Won")

        fig, ax = plt.subplots(figsize=(10, 5))

        winner_counts.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_xlabel("Matches Won")
        ax.set_ylabel("Teams")

        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Winner Statistics")

        st.dataframe(
            winner_counts.reset_index().rename(
                columns={
                    "index": "Team",
                    "winner": "Matches Won"
                }
            ),
            use_container_width=True
        )

    else:
        st.info("No match winner data available.")

# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

st.markdown(
    "<center>🏏 IPL Cricket Performance Dashboard | "
    "Developed using Python, Pandas, Matplotlib and Streamlit</center>",
    unsafe_allow_html=True
)
