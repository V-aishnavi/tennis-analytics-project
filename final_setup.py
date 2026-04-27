import sqlite3

conn = sqlite3.connect('tennis_analytics.db')
cursor = conn.cursor()

print("="*70)
print("TENNIS ANALYTICS - COMPLETE SQL QUERY RESULTS")
print("="*70)

print("\nCOMPETITIONS ANALYSIS")
print("-"*50)

print("\n1. List all competitions with their category names (first 10):")
cursor.execute("""
    SELECT c.competition_name, cat.category_name
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} -> {row[1]}")

print("\n2. Count the number of competitions in each category:")
cursor.execute("""
    SELECT cat.category_name, COUNT(*) as count
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} competitions")

print("\n3. Find all competitions of type 'doubles' (first 10):")
cursor.execute("""
    SELECT competition_name, gender
    FROM Competitions
    WHERE type = 'doubles'
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]})")

print("\n4. Get competitions that belong to ITF Men category (first 10):")
cursor.execute("""
    SELECT c.competition_name, c.type, c.gender
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    WHERE cat.category_name = 'ITF Men'
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]}/{row[2]}")

print("\n5. Identify parent competitions and their sub-competitions (top 10):")
cursor.execute("""
    SELECT parent.competition_name as Parent, COUNT(child.competition_id) as Sub_Count
    FROM Competitions parent
    JOIN Competitions child ON parent.competition_id = child.parent_id
    GROUP BY parent.competition_id
    ORDER BY Sub_Count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} sub-competitions")

print("\n6. Analyze distribution of competition types by category (first 15):")
cursor.execute("""
    SELECT cat.category_name, c.type, COUNT(*) as count
    FROM Competitions c
    JOIN Categories cat ON c.category_id = cat.category_id
    GROUP BY cat.category_name, c.type
    ORDER BY cat.category_name, count DESC
    LIMIT 15
""")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]}: {row[2]}")

print("\n7. List all top-level competitions (no parent) (first 10):")
cursor.execute("""
    SELECT competition_name, type, gender
    FROM Competitions
    WHERE parent_id IS NULL
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}/{row[2]})")

print("\n\nVENUE ANALYSIS")
print("-"*50)

print("\n8. List all venues with their associated complex names (first 10):")
cursor.execute("""
    SELECT v.venue_name, c.complex_name, v.country_name
    FROM Venues v
    JOIN Complexes c ON v.complex_id = c.complex_id
    WHERE v.country_name != ''
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} -> {row[1]} ({row[2]})")

print("\n9. Count the number of venues in each complex (top 10):")
cursor.execute("""
    SELECT c.complex_name, COUNT(v.venue_id) as venue_count
    FROM Complexes c
    LEFT JOIN Venues v ON c.complex_id = v.complex_id
    GROUP BY c.complex_id
    ORDER BY venue_count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} venues")

print("\n10. Get details of venues in a specific country (Spain) (first 10):")
cursor.execute("""
    SELECT venue_name, city_name, timezone
    FROM Venues
    WHERE country_name = 'Spain'
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]}) - {row[2]}")

print("\n11. Identify all venues with their timezones (first 10):")
cursor.execute("""
    SELECT venue_name, timezone, country_name
    FROM Venues
    WHERE timezone != '' AND timezone IS NOT NULL
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]} - {row[1]} ({row[2]})")

print("\n12. Find complexes with more than one venue (top 10):")
cursor.execute("""
    SELECT c.complex_name, COUNT(v.venue_id) as venue_count
    FROM Complexes c
    JOIN Venues v ON c.complex_id = v.complex_id
    GROUP BY c.complex_id
    HAVING venue_count > 1
    ORDER BY venue_count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} venues")

print("\n13. List venues grouped by country (top 10):")
cursor.execute("""
    SELECT country_name, COUNT(*) as count
    FROM Venues
    WHERE country_name != ''
    GROUP BY country_name
    ORDER BY count DESC
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} venues")

print("\n14. Find all venues for a specific complex (Nacional):")
cursor.execute("""
    SELECT v.venue_name, v.city_name
    FROM Venues v
    JOIN Complexes c ON v.complex_id = c.complex_id
    WHERE c.complex_name = 'Nacional'
""")
for row in cursor.fetchall():
    print(f"   {row[0]} ({row[1]})")

print("\n\nRANKING ANALYSIS")
print("-"*50)

print("\n15. Get all competitors with their rank and points:")
cursor.execute("""
    SELECT c.name, r.rank, r.points, c.country
    FROM Competitors c
    JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.rank
""")
for row in cursor.fetchall():
    print(f"   #{row[1]}: {row[0]} - {row[2]} points ({row[3]})")

print("\n16. Find competitors ranked in the top 5:")
cursor.execute("""
    SELECT c.name, r.rank, r.points, c.country
    FROM Competitors c
    JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
    WHERE r.rank <= 5
    ORDER BY r.rank
""")
for row in cursor.fetchall():
    print(f"   #{row[1]}: {row[0]} from {row[3]} - {row[2]} points")

print("\n17. List competitors with no rank movement (stable rank):")
cursor.execute("""
    SELECT c.name, r.rank, r.movement, r.points
    FROM Competitors c
    JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
    WHERE r.movement = 0
""")
for row in cursor.fetchall():
    print(f"   {row[0]} - Rank {row[1]} (Movement: {row[2]}) - {row[3]} points")

print("\n18. Get total points of competitors from a specific country (Serbia):")
cursor.execute("""
    SELECT c.country, SUM(r.points) as total_points, COUNT(*) as num_players
    FROM Competitors c
    JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
    WHERE c.country = 'Serbia'
    GROUP BY c.country
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} total points from {row[2]} player(s)")

print("\n19. Count competitors per country:")
cursor.execute("""
    SELECT country, COUNT(*) as count
    FROM Competitors
    GROUP BY country
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} competitors")

print("\n20. Find competitors with the highest points in the current week:")
cursor.execute("""
    SELECT c.name, r.points, r.rank, c.country
    FROM Competitors c
    JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.points DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"   #{row[2]}: {row[0]} - {row[1]} points ({row[3]})")

conn.close()

print("\n" + "="*70)
print("ALL 20 SQL QUERIES COMPLETED SUCCESSFULLY")
print("="*70)
print("\nQueries included:")
print("  - Competitions Analysis: 7 queries")
print("  - Venue Analysis: 7 queries")
print("  - Ranking Analysis: 6 queries")
print("  - Total: 20 queries")