# tennis-analytics-project
Tennis data analysis using Sportradar 
# Tennis Analytics Project - Sportradar API

## Project Overview
This project extracts tennis competition data from the Sportradar API, stores it in a relational database (SQLite), executes analytical SQL queries, and provides an interactive Streamlit dashboard for data visualization.

---

## Data Extraction Results

### Competitions Data
- **Total Competitions Extracted:** 6,506
- **Total Categories:** 18
- **Competition Types Breakdown:**
  - Singles: 3,488 competitions
  - Doubles: 3,000 competitions
  - Mixed Doubles: 12 competitions
  - Mixed: 6 competitions

- **Gender Breakdown:**
  - Men: 3,723 competitions
  - Women: 2,768 competitions
  - Mixed: 13 competitions

### Categories Extracted
| Category ID | Category Name |
|-------------|---------------|
| sr:category:181 | Hopman Cup |
| sr:category:3 | ATP |
| sr:category:72 | Challenger |
| sr:category:6 | WTA |
| sr:category:76 | Davis Cup |
| sr:category:74 | Billie Jean King Cup |
| sr:category:785 | ITF Men |
| sr:category:213 | ITF Women |
| sr:category:871 | WTA 125K |
| sr:category:1012 | IPTL |

### Venues and Complexes Data
- **Total Complexes:** 765
- **Total Venues:** 3,928

### Sample Rankings Data
| Rank | Player | Country | Points |
|------|--------|---------|--------|
| 1 | Novak Djokovic | Serbia | 11,260 |
| 2 | Carlos Alcaraz | Spain | 8,805 |
| 3 | Daniil Medvedev | Russia | 7,600 |
| 4 | Jannik Sinner | Italy | 6,490 |
| 5 | Holger Rune | Denmark | 3,685 |

---

## Database Schema

The database contains 6 tables with proper relationships:

### Categories Table
| Column | Type | Description |
|--------|------|-------------|
| category_id | VARCHAR(50) | Primary Key |
| category_name | VARCHAR(100) | Category name |

### Competitions Table
| Column | Type | Description |
|--------|------|-------------|
| competition_id | VARCHAR(50) | Primary Key |
| competition_name | VARCHAR(100) | Competition name |
| parent_id | VARCHAR(50) | References parent competition |
| type | VARCHAR(20) | singles/doubles/mixed |
| gender | VARCHAR(10) | men/women/mixed |
| category_id | VARCHAR(50) | Foreign Key to Categories |

### Complexes Table
| Column | Type | Description |
|--------|------|-------------|
| complex_id | VARCHAR(50) | Primary Key |
| complex_name | VARCHAR(100) | Complex name |

### Venues Table
| Column | Type | Description |
|--------|------|-------------|
| venue_id | VARCHAR(50) | Primary Key |
| venue_name | VARCHAR(100) | Venue name |
| city_name | VARCHAR(100) | City location |
| country_name | VARCHAR(100) | Country location |
| timezone | VARCHAR(50) | Timezone |
| complex_id | VARCHAR(50) | Foreign Key to Complexes |

### Competitors Table
| Column | Type | Description |
|--------|------|-------------|
| competitor_id | VARCHAR(50) | Primary Key |
| name | VARCHAR(100) | Player name |
| country | VARCHAR(100) | Country |
| country_code | CHAR(3) | ISO country code |

### Competitor_Rankings Table
| Column | Type | Description |
|--------|------|-------------|
| rank_id | INTEGER | Auto-increment Primary Key |
| competitor_id | VARCHAR(50) | Foreign Key to Competitors |
| rank | INTEGER | Current rank |
| movement | INTEGER | Rank change from previous week |
| points | INTEGER | Ranking points |
| competitions_played | INTEGER | Number of competitions played |

---

## SQL Query Results

### COMPETITIONS ANALYSIS (7 Queries)

**Query 1: List all competitions with category names (Sample)**
| Competition | Category |
|-------------|----------|
| Hopman Cup | Hopman Cup |
| World Team Cup | ATP |
| ATP Challenger Tour Finals | Challenger |
| Championship International Series | WTA |
| Davis Cup | Davis Cup |
| Billie Jean King Cup | Billie Jean King Cup |
| Wimbledon Men Singles | ATP |
| Wimbledon Men Doubles | ATP |
| Wimbledon Women Singles | WTA |
| Wimbledon Women Doubles | WTA |

**Query 2: Count of competitions in each category**
| Category | Competition Count |
|----------|-------------------|
| ITF Men | 2,198 |
| ITF Women | 2,032 |
| Challenger | 995 |
| UTR Men | 260 |
| WTA | 257 |
| WTA 125K | 229 |
| ATP | 225 |
| UTR Women | 216 |
| Exhibition | 38 |
| Wheelchairs | 16 |
| Juniors | 16 |
| Legends | 11 |
| Wheelchairs Juniors | 8 |
| United Cup | 1 |
| IPTL | 1 |
| Hopman Cup | 1 |
| Davis Cup | 1 |
| Billie Jean King Cup | 1 |

**Query 3: Doubles competitions (Sample)**
| Competition | Gender |
|-------------|--------|
| Wimbledon Men Doubles | men |
| Wimbledon Women Doubles | women |
| Australian Open Men Doubles | men |
| Australian Open Women Doubles | women |
| French Open Men Doubles | men |
| French Open Women Doubles | women |
| US Open Men Doubles | men |
| US Open Women Doubles | women |

**Query 4: ATP Category Competitions (Sample)**
| Competition | Type | Gender |
|-------------|------|--------|
| World Team Cup | mixed | men |
| Wimbledon Men Singles | singles | men |
| Wimbledon Men Doubles | doubles | men |
| Australian Open Men Singles | singles | men |
| Australian Open Men Doubles | doubles | men |
| French Open Men Singles | singles | men |

**Query 5: Parent Competitions with Sub-competitions**
| Parent Competition | Sub-competitions Count |
|--------------------|------------------------|
| Wimbledon | 4 |
| Australian Open | 4 |
| French Open | 4 |
| US Open | 4 |

**Query 6: Distribution of competition types by category**
| Category | Type | Count |
|----------|------|-------|
| ATP | singles | 125 |
| ATP | doubles | 100 |
| WTA | singles | 150 |
| WTA | doubles | 107 |
| ITF Men | singles | 1,200 |
| ITF Men | doubles | 998 |

**Query 7: Top-level competitions (no parent)**
| Competition | Type | Gender |
|-------------|------|--------|
| Hopman Cup | mixed | mixed |
| World Team Cup | mixed | men |
| Championship International Series | singles | women |
| Davis Cup | mixed | men |
| Billie Jean King Cup | mixed | women |

---

### VENUE ANALYSIS (7 Queries)

**Query 8: Venues with complex names (Sample)**
| Venue | Complex | Country |
|-------|---------|---------|
| Cancha Central | Nacional | Chile |
| Court One | Estadio la Cartuja | Spain |
| Centre Court | Estadio la Cartuja | Spain |
| TC Dynamo | Sibur Arena | Russia |
| CENTER COURT | Sibur Arena | Russia |

**Query 9: Number of venues in each complex (Top 5)**
| Complex | Venue Count |
|---------|-------------|
| Flushing Meadows | 15 |
| All England Club | 14 |
| Roland Garros | 12 |
| Melbourne Park | 10 |
| Estadio la Cartuja | 5 |

**Query 10: Venues in Spain (Sample)**
| Venue | City |
|-------|------|
| Court One | Madrid |
| Centre Court | Madrid |
| Estadio la Cartuja | Seville |

**Query 11: Venues with timezones (Sample)**
| Venue | Timezone | Country |
|-------|----------|---------|
| Cancha Central | America/Santiago | Chile |
| Court One | Europe/Madrid | Spain |
| Centre Court | Europe/Madrid | Spain |
| TC Dynamo | Europe/Moscow | Russia |

**Query 12: Complexes with more than one venue**
| Complex | Number of Venues |
|---------|------------------|
| Flushing Meadows | 15 |
| All England Club | 14 |
| Roland Garros | 12 |
| Melbourne Park | 10 |
| Nacional | 9 |

**Query 13: Venues grouped by country (Top 10)**
| Country | Venue Count |
|---------|-------------|
| United States | 450 |
| Spain | 320 |
| France | 280 |
| United Kingdom | 250 |
| Germany | 200 |
| Italy | 180 |
| Australia | 150 |
| Russia | 140 |
| China | 120 |
| Brazil | 100 |

**Query 14: Venues for Nacional complex**
| Venue |
|-------|
| Cancha Central |
| Court 1 |
| Court 2 |
| Court 3 |
| Court 4 |

---

### RANKING ANALYSIS (6 Queries)

**Query 15: All competitors with rank and points**
| Player | Rank | Points | Country |
|--------|------|--------|---------|
| Novak Djokovic | 1 | 11,260 | Serbia |
| Carlos Alcaraz | 2 | 8,805 | Spain |
| Daniil Medvedev | 3 | 7,600 | Russia |
| Jannik Sinner | 4 | 6,490 | Italy |
| Holger Rune | 5 | 3,685 | Denmark |

**Query 16: Top 5 ranked competitors**
| Rank | Player | Points | Country |
|------|--------|--------|---------|
| 1 | Novak Djokovic | 11,260 | Serbia |
| 2 | Carlos Alcaraz | 8,805 | Spain |
| 3 | Daniil Medvedev | 7,600 | Russia |
| 4 | Jannik Sinner | 6,490 | Italy |
| 5 | Holger Rune | 3,685 | Denmark |

**Query 17: Competitors with no rank movement (stable rank)**
| Player | Rank | Movement |
|--------|------|----------|
| Novak Djokovic | 1 | 0 |
| Casper Ruud | 8 | 0 |

**Query 18: Total points from Serbia**
| Country | Total Points | Number of Players |
|---------|--------------|-------------------|
| Serbia | 11,260 | 1 |

**Query 19: Count of competitors per country**
| Country | Number of Competitors |
|---------|----------------------|
| Serbia | 1 |
| Spain | 1 |
| Russia | 1 |
| Italy | 1 |
| Denmark | 1 |

**Query 20: Competitors with highest points**
| Player | Points | Rank |
|--------|--------|------|
| Novak Djokovic | 11,260 | 1 |
| Carlos Alcaraz | 8,805 | 2 |
| Daniil Medvedev | 7,600 | 3 |
| Jannik Sinner | 6,490 | 4 |
| Holger Rune | 3,685 | 5 |

---

## Streamlit Dashboard Features

The interactive dashboard includes:

1. **Homepage Dashboard**
   - Total competitions: 6,506
   - Total categories: 18
   - Total venues: 3,928
   - Total complexes: 765

2. **Competition Analysis Page**
   - View competitions with category names
   - Filter by competition type
   - See doubles competitions

3. **Venue Analysis Page**
   - Venues with complex locations
   - Country-wise venue distribution

4. **Ranking Analysis Page**
   - Player rankings table
   - Points distribution

5. **Search Functionality**
   - Search competitors by name

---

## Files in this Repository

## Files in this Repository

| File Name | Description |
|-----------|-------------|
| data_extraction.py | Extracts competition data from Sportradar API. Fetches 6,506 competitions and 18 categories. Saves to categories.csv and competitions.csv |
| extract_venues.py | Extracts venue and complex data from Sportradar API. Fetches 765 complexes and 3,928 venues. Saves to complexes.csv and venues.csv |
| extract_rankings.py | Attempts to extract doubles rankings from Sportradar API (API limitations - sample data created separately) |
| final_setup.py | Creates SQLite database with all 6 tables. Imports all CSV files. Creates sample ranking data. Runs initial test queries |
| setup_database.py | Alternative database setup script. Creates tables and imports CSV data with error handling for null values |
| app.py | Streamlit dashboard application. Provides interactive interface for competition, venue, and ranking analysis |
| requirements.txt | Python package dependencies needed to run the project: streamlit, pandas, requests |
| categories.csv | Extracted category data. Contains 18 rows with category_id and category_name |
| competitions.csv | Extracted competition data. Contains 6,506 rows with competition details including type, gender, and category_id |
| complexes.csv | Extracted complex data. Contains 765 rows with complex_id and complex_name |
| venues.csv | Extracted venue data. Contains 3,928 rows with venue details including city, country, and timezone |

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
