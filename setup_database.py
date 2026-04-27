import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text, inspect

# Database connection settings
# For MySQL:
# DB_URL = "mysql+pymysql://username:password@localhost:3306/tennis_db"
# For PostgreSQL:
DB_URL = "postgresql://postgres:your_password@localhost:5432/tennis_db"

# Using SQLite for now (no installation needed, good for testing)
# We'll use SQLite to get started, then you can switch to MySQL/PostgreSQL
import sqlite3

def create_sqlite_connection():
    """Create SQLite database connection (no setup required)"""
    conn = sqlite3.connect('tennis_analytics.db')
    return conn

def create_tables(conn):
    """Create all tables based on the assignment schema"""
    
    cursor = conn.cursor()
    
    # 1. Categories Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id VARCHAR(50) PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
        )
    ''')
    
    # 2. Competitions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Competitions (
            competition_id VARCHAR(50) PRIMARY KEY,
            competition_name VARCHAR(100) NOT NULL,
            parent_id VARCHAR(50),
            type VARCHAR(20) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            category_id VARCHAR(50),
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )
    ''')
    
    # 3. Complexes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Complexes (
            complex_id VARCHAR(50) PRIMARY KEY,
            complex_name VARCHAR(100) NOT NULL
        )
    ''')
    
    # 4. Venues Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Venues (
            venue_id VARCHAR(50) PRIMARY KEY,
            venue_name VARCHAR(100) NOT NULL,
            city_name VARCHAR(100),
            country_name VARCHAR(100),
            timezone VARCHAR(50),
            complex_id VARCHAR(50),
            FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
        )
    ''')
    
    # 5. Competitors Table (for rankings - we'll create with sample data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Competitors (
            competitor_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL
        )
    ''')
    
    # 6. Competitor_Rankings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Competitor_Rankings (
            rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor_id VARCHAR(50),
            rank INTEGER NOT NULL,
            movement INTEGER NOT NULL,
            points INTEGER NOT NULL,
            competitions_played INTEGER NOT NULL,
            FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
        )
    ''')
    
    conn.commit()
    print("All tables created successfully!")

def import_csv_to_tables(conn):
    """Import CSV data into respective tables"""
    
    # Import Categories
    categories_df = pd.read_csv('categories.csv')
    categories_df.to_sql('Categories', conn, if_exists='replace', index=False)
    print(f" Imported {len(categories_df)} categories")
    
    # Import Competitions
    competitions_df = pd.read_csv('competitions.csv')
    # Handle NaN values in parent_id
    competitions_df['parent_id'] = competitions_df['parent_id'].where(pd.notna(competitions_df['parent_id']), None)
    competitions_df.to_sql('Competitions', conn, if_exists='replace', index=False)
    print(f" Imported {len(competitions_df)} competitions")
    
    # Import Complexes (if file exists)
    try:
        complexes_df = pd.read_csv('complexes.csv')
        complexes_df.to_sql('Complexes', conn, if_exists='replace', index=False)
        print(f" Imported {len(complexes_df)} complexes")
    except FileNotFoundError:
        print(" complexes.csv not found - run extract_venues.py first")
    
    # Import Venues (if file exists)
    try:
        venues_df = pd.read_csv('venues.csv')
        venues_df.to_sql('Venues', conn, if_exists='replace', index=False)
        print(f" Imported {len(venues_df)} venues")
    except FileNotFoundError:
        print("venues.csv not found - run extract_venues.py first")
    
    # Create sample ranking data if real data not available
    create_sample_rankings_data(conn)

def create_sample_rankings_data(conn):
    """Create sample competitor and ranking data for demonstration"""
    
    cursor = conn.cursor()
    
    # Sample top tennis players for demonstration
    sample_competitors = [
        ('comp_001', 'Novak Djokovic', 'Serbia', 'SRB'),
        ('comp_002', 'Carlos Alcaraz', 'Spain', 'ESP'),
        ('comp_003', 'Daniil Medvedev', 'Russia', 'RUS'),
        ('comp_004', 'Jannik Sinner', 'Italy', 'ITA'),
        ('comp_005', 'Holger Rune', 'Denmark', 'DEN'),
        ('comp_006', 'Andrey Rublev', 'Russia', 'RUS'),
        ('comp_007', 'Stefanos Tsitsipas', 'Greece', 'GRE'),
        ('comp_008', 'Casper Ruud', 'Norway', 'NOR'),
        ('comp_009', 'Alexander Zverev', 'Germany', 'GER'),
        ('comp_010', 'Taylor Fritz', 'USA', 'USA'),
    ]
    
    sample_rankings = [
        (1, 'comp_001', 1, 0, 11260, 18),
        (2, 'comp_002', 2, 1, 8805, 20),
        (3, 'comp_003', 3, -1, 7600, 19),
        (4, 'comp_004', 4, 2, 6490, 17),
        (5, 'comp_005', 5, -1, 3685, 22),
        (6, 'comp_006', 6, 1, 3615, 21),
        (7, 'comp_007', 7, -2, 3570, 20),
        (8, 'comp_008', 8, 0, 3450, 19),
        (9, 'comp_009', 9, 1, 3165, 18),
        (10, 'comp_010', 10, -1, 3050, 22),
    ]
    
    # Clear existing data
    cursor.execute("DELETE FROM Competitor_Rankings")
    cursor.execute("DELETE FROM Competitors")
    
    # Insert sample competitors
    for comp in sample_competitors:
        cursor.execute('''
            INSERT OR REPLACE INTO Competitors 
            (competitor_id, name, country, country_code)
            VALUES (?, ?, ?, ?)
        ''', comp)
    
    # Insert sample rankings
    for rank in sample_rankings:
        cursor.execute('''
            INSERT INTO Competitor_Rankings 
            (rank_id, competitor_id, rank, movement, points, competitions_played)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', rank)
    
    conn.commit()
    print(f"✅ Created sample data: {len(sample_competitors)} competitors with rankings")

def test_queries(conn):
    """Test some of the required SQL queries"""
    
    print("\n" + "="*60)
    print("TESTING SQL QUERIES")
    print("="*60)
    
    cursor = conn.cursor()
    
    # Query 1: List all competitions with category names
    print("\n1. Competitions with their category names (first 5):")
    cursor.execute('''
        SELECT c.competition_name, cat.category_name
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   • {row[0]} → {row[1]}")
    
    # Query 2: Count competitions in each category
    print("\n2. Number of competitions per category:")
    cursor.execute('''
        SELECT cat.category_name, COUNT(*) as comp_count
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name
        ORDER BY comp_count DESC
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   • {row[0]}: {row[1]} competitions")
    
    # Query 3: Find competitions of type 'doubles'
    print("\n3. Doubles competitions (first 5):")
    cursor.execute('''
        SELECT competition_name, gender
        FROM Competitions
        WHERE type = 'doubles'
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   • {row[0]} ({row[1]})")
    
    # Query 4: Top level competitions (no parent)
    print("\n4. Top-level competitions (first 5):")
    cursor.execute('''
        SELECT competition_name, type, gender
        FROM Competitions
        WHERE parent_id IS NULL
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   • {row[0]} - {row[1]}/{row[2]}")
    
    # Query 5: Sample ranking query
    print("\n5. Top 5 ranked competitors:")
    cursor.execute('''
        SELECT r.rank, c.name, c.country, r.points
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        ORDER BY r.rank
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   • #{row[0]}: {row[1]} ({row[2]}) - {row[3]} points")

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("SETTING UP TENNIS ANALYTICS DATABASE")
    print("="*60)
    
    # Create SQLite database (no setup needed)
    conn = create_sqlite_connection()
    
    # Create tables
    create_tables(conn)
    
    # Import CSV data
    import_csv_to_tables(conn)
    
    # Test queries
    test_queries(conn)
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print("\nDatabase file created: tennis_analytics.db")
    print("\nYou can now: ")
    print("1. Run SQL queries on this database")
    print("2. Build Streamlit app connected to this database")
    
    conn.close()