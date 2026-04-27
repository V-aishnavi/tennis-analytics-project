import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Tennis Analytics Dashboard", layout="wide")

st.title("Tennis Analytics Dashboard")
st.markdown("---")

def get_connection():
    return sqlite3.connect('tennis_analytics.db', check_same_thread=False)

def run_query(query, params=()):
    conn = get_connection()
    try:
        result = pd.read_sql_query(query, conn, params=params)
        return result
    finally:
        conn.close()

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Homepage Dashboard", "Competition Analysis", "Venue Analysis", "Ranking Analysis", "Search & Filter"])

if page == "Homepage Dashboard":
    st.header("Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_competitions = run_query("SELECT COUNT(*) as count FROM Competitions")
        st.metric("Total Competitions", total_competitions.iloc[0,0])
    
    with col2:
        total_categories = run_query("SELECT COUNT(*) as count FROM Categories")
        st.metric("Total Categories", total_categories.iloc[0,0])
    
    with col3:
        total_venues = run_query("SELECT COUNT(*) as count FROM Venues")
        st.metric("Total Venues", total_venues.iloc[0,0])
    
    with col4:
        total_complexes = run_query("SELECT COUNT(*) as count FROM Complexes")
        st.metric("Total Complexes", total_complexes.iloc[0,0])
    
    st.markdown("---")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("Competitions by Type")
        type_dist = run_query("""
            SELECT type, COUNT(*) as count 
            FROM Competitions 
            GROUP BY type 
            ORDER BY count DESC
        """)
        if not type_dist.empty:
            st.bar_chart(type_dist.set_index('type'))
    
    with col6:
        st.subheader("Competitions by Gender")
        gender_dist = run_query("""
            SELECT gender, COUNT(*) as count 
            FROM Competitions 
            WHERE gender != 'unknown'
            GROUP BY gender 
            ORDER BY count DESC
        """)
        if not gender_dist.empty:
            st.bar_chart(gender_dist.set_index('gender'))
    
    st.subheader("Top 5 Categories by Competition Count")
    top_categories = run_query("""
        SELECT cat.category_name, COUNT(*) as count
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name
        ORDER BY count DESC
        LIMIT 5
    """)
    if not top_categories.empty:
        st.dataframe(top_categories, use_container_width=True)

elif page == "Competition Analysis":
    st.header("Competition Analysis")
    
    analysis_type = st.selectbox("Select Analysis", [
        "Competitions with Category Names",
        "Competitions by Category Count",
        "Doubles Competitions",
        "Top Level Competitions",
        "Parent Competitions with Sub-competitions"
    ])
    
    if analysis_type == "Competitions with Category Names":
        query = """
            SELECT c.competition_name, cat.category_name, c.type, c.gender
            FROM Competitions c
            JOIN Categories cat ON c.category_id = cat.category_id
            LIMIT 50
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Competitions by Category Count":
        query = """
            SELECT cat.category_name, COUNT(*) as count
            FROM Competitions c
            JOIN Categories cat ON c.category_id = cat.category_id
            GROUP BY cat.category_name
            ORDER BY count DESC
        """
        df = run_query(query)
        if not df.empty:
            st.bar_chart(df.set_index('category_name'))
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Doubles Competitions":
        query = """
            SELECT competition_name, gender, category_id
            FROM Competitions
            WHERE type = 'doubles'
            LIMIT 50
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Top Level Competitions":
        query = """
            SELECT c.competition_name, c.type, c.gender, cat.category_name
            FROM Competitions c
            JOIN Categories cat ON c.category_id = cat.category_id
            WHERE parent_id IS NULL
            LIMIT 50
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Parent Competitions with Sub-competitions":
        query = """
            SELECT parent.competition_name as Parent, 
                   COUNT(child.competition_id) as Sub_competitions
            FROM Competitions parent
            JOIN Competitions child ON parent.competition_id = child.parent_id
            GROUP BY parent.competition_id
            ORDER BY Sub_competitions DESC
            LIMIT 20
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)

elif page == "Venue Analysis":
    st.header("Venue Analysis")
    
    analysis_type = st.selectbox("Select Analysis", [
        "Venues with Complex Names",
        "Venues by Country",
        "Complexes with Multiple Venues",
        "Venues by Timezone"
    ])
    
    if analysis_type == "Venues with Complex Names":
        query = """
            SELECT v.venue_name, c.complex_name, v.city_name, v.country_name
            FROM Venues v
            JOIN Complexes c ON v.complex_id = c.complex_id
            WHERE v.country_name != ''
            LIMIT 50
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Venues by Country":
        query = """
            SELECT country_name, COUNT(*) as count
            FROM Venues
            WHERE country_name != ''
            GROUP BY country_name
            ORDER BY count DESC
            LIMIT 20
        """
        df = run_query(query)
        if not df.empty:
            st.bar_chart(df.set_index('country_name'))
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Complexes with Multiple Venues":
        query = """
            SELECT c.complex_name, COUNT(v.venue_id) as venue_count
            FROM Complexes c
            JOIN Venues v ON c.complex_id = v.complex_id
            GROUP BY c.complex_id
            HAVING venue_count > 1
            ORDER BY venue_count DESC
            LIMIT 20
        """
        df = run_query(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
    
    elif analysis_type == "Venues by Timezone":
        query = """
            SELECT timezone, COUNT(*) as count
            FROM Venues
            WHERE timezone != '' AND timezone IS NOT NULL
            GROUP BY timezone
            ORDER BY count DESC
            LIMIT 15
        """
        df = run_query(query)
        if not df.empty:
            st.bar_chart(df.set_index('timezone'))

elif page == "Ranking Analysis":
    st.header("Ranking Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Ranked Competitors")
        top_ranked = run_query("""
            SELECT c.name, r.rank, r.points, c.country, r.competitions_played
            FROM Competitors c
            JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
            ORDER BY r.rank
        """)
        if not top_ranked.empty:
            st.dataframe(top_ranked, use_container_width=True)
    
    with col2:
        st.subheader("Competitors by Country")
        country_count = run_query("""
            SELECT country, COUNT(*) as count
            FROM Competitors
            GROUP BY country
        """)
        if not country_count.empty:
            st.dataframe(country_count, use_container_width=True)
    
    st.subheader("Points Distribution")
    points_data = run_query("""
        SELECT c.name, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
        ORDER BY r.rank
    """)
    if not points_data.empty:
        st.bar_chart(points_data.set_index('name'))

elif page == "Search & Filter":
    st.header("Search and Filter Competitors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_name = st.text_input("Search by competitor name", "")
    
    with col2:
        rank_limit = st.number_input("Filter by rank (top N)", min_value=1, max_value=100, value=10)
    
    competitors_df = run_query("SELECT DISTINCT country FROM Competitors")
    countries = ["All"] + competitors_df['country'].tolist() if not competitors_df.empty else ["All"]
    country_filter = st.selectbox("Filter by country", countries)
    
    points_threshold = st.slider("Minimum points", min_value=0, max_value=12000, value=0)
    
    query = """
        SELECT c.name, r.rank, r.points, c.country, r.competitions_played, r.movement
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
        WHERE r.rank <= ?
    """
    params = [rank_limit]
    
    if search_name:
        query += " AND c.name LIKE ?"
        params.append(f"%{search_name}%")
    
    if country_filter != "All":
        query += " AND c.country = ?"
        params.append(country_filter)
    
    if points_threshold > 0:
        query += " AND r.points >= ?"
        params.append(points_threshold)
    
    query += " ORDER BY r.rank"
    
    results = run_query(query, params)
    
    st.subheader(f"Found {len(results)} competitors")
    if not results.empty:
        st.dataframe(results, use_container_width=True)

st.markdown("---")
st.caption("Data source: Sportradar API | Tennis Analytics Dashboard")