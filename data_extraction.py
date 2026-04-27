import requests
import json
import pandas as pd

API_KEY = "wJU8Lwraqz1Y3xaAvcuw9OIkEX8dAReatoHtWMZe"  # Your working key

def fetch_competitions_data():
    """Fetches competition data from Sportradar API"""
    
    base_url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"
    params = {'api_key': API_KEY}
    
    try:
        print("Fetching competitions data...")
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(" Successfully fetched data!")
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def parse_competitions_data(data):
    """
    Parses the JSON data into Categories and Competitions tables
    Based on the actual API response structure
    """
    
    categories_dict = {}  # To store unique categories
    competitions = []
    
    if not data or 'competitions' not in data:
        print("No competitions data found")
        return [], []
    
    print(f"\nProcessing {len(data['competitions'])} competitions...")
    
    for competition in data['competitions']:
        # Extract category info (if exists)
        category_id = None
        category_name = None
        
        if 'category' in competition:
            category = competition['category']
            category_id = category.get('id')
            category_name = category.get('name')
            
            # Add to categories dictionary if unique
            if category_id and category_id not in categories_dict:
                categories_dict[category_id] = {
                    'category_id': category_id,
                    'category_name': category_name
                }
        
        # Create competition record
        competition_record = {
            'competition_id': competition.get('id', ''),
            'competition_name': competition.get('name', ''),
            'parent_id': competition.get('parent_id'),  # Nullable
            'type': competition.get('type', ''),
            'gender': competition.get('gender', ''),
            'category_id': category_id
        }
        competitions.append(competition_record)
    
    # Convert categories dict to list
    categories = list(categories_dict.values())
    
    print(f" Parsed {len(categories)} categories and {len(competitions)} competitions")
    return categories, competitions

def save_to_csv(categories, competitions):
    """Saves the parsed data to CSV files"""
    
    categories_df = pd.DataFrame(categories)
    competitions_df = pd.DataFrame(competitions)
    
    categories_df.to_csv('categories.csv', index=False)
    competitions_df.to_csv('competitions.csv', index=False)
    
    print("\n Data saved to CSV files:")
    print(f"   - categories.csv ({len(categories)} rows)")
    print(f"   - competitions.csv ({len(competitions)} rows)")
    
    return categories_df, competitions_df

def preview_data(categories_df, competitions_df):
    """Display preview of the data"""
    
    print("\n" + "="*60)
    print("DATA PREVIEW")
    print("="*60)
    
    print("\n Categories Table Preview:")
    print(categories_df.head(10).to_string())
    
    print("\n Competitions Table Preview (first 10 rows):")
    print(competitions_df.head(10).to_string())
    
    print("\n Quick Statistics:")
    print(f"   - Total Competitions: {len(competitions_df)}")
    print(f"   - Unique Categories: {len(categories_df)}")
    print(f"   - Competition Types: {competitions_df['type'].value_counts().to_dict()}")
    print(f"   - Genders: {competitions_df['gender'].value_counts().to_dict()}")

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("TENNIS DATA EXTRACTION - SPORTRADAR API")
    print("="*60)
    
    # Step 1: Fetch data
    raw_data = fetch_competitions_data()
    
    if raw_data:
        # Step 2: Parse nested JSON
        categories, competitions = parse_competitions_data(raw_data)
        
        # Step 3: Save to CSV
        categories_df, competitions_df = save_to_csv(categories, competitions)
        
        # Step 4: Preview the data
        preview_data(categories_df, competitions_df)
        
        print("\n" + "="*60)
        print(" COMPETITION DATA EXTRACTION COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Extract Complexes & Venues data")
        print("2. Extract Doubles Competitor Rankings data")
        print("3. Create SQL database and import data")
        
    else:
        print(" Failed to fetch data")