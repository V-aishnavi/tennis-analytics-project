import requests
import pandas as pd

API_KEY = "wJU8Lwraqz1Y3xaAvcuw9OIkEX8dAReatoHtWMZe"

def fetch_doubles_rankings():
    """
    Fetches doubles competitor rankings from Sportradar API
    Endpoint: Doubles Competitor Rankings API
    """
    
    # Note: You might need to specify a date or season
    # Common formats: /rankings/doubles.json or /rankings/doubles/2025/02/rankings.json
    
    base_url = "https://api.sportradar.com/tennis/trial/v3/en/rankings/doubles.json"
    params = {'api_key': API_KEY}
    
    try:
        print("Fetching doubles rankings data...")
        print(f"URL: {base_url}")
        response = requests.get(base_url, params=params)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f" Successfully fetched data!")
            print(f"   Response keys: {data.keys() if isinstance(data, dict) else 'List response'}")
            return data
        else:
            print(f" Could not fetch rankings. Trying alternative endpoint...")
            # Try alternative endpoint
            alt_url = "https://api.sportradar.com/tennis/trial/v3/en/doubles_rankings.json"
            response = requests.get(alt_url, params=params)
            print(f"Alternative URL Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def parse_rankings_data(data):
    """
    Parses rankings data into Competitor_Rankings and Competitors tables
    """
    
    rankings = []
    competitors = {}
    
    # Handle different possible response structures
    rankings_list = []
    
    if isinstance(data, dict):
        if 'rankings' in data:
            rankings_list = data['rankings']
        elif 'competitors' in data:
            rankings_list = data['competitors']
        else:
            # Try to find list in response
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    rankings_list = value
                    print(f"Found rankings in key: '{key}'")
                    break
    elif isinstance(data, list):
        rankings_list = data
    else:
        print(f"Unexpected data type: {type(data)}")
        return [], []
    
    print(f"\nProcessing {len(rankings_list)} ranking records...")
    
    for idx, item in enumerate(rankings_list):
        # Extract competitor info
        competitor_id = item.get('competitor_id') or item.get('id', '')
        competitor_name = item.get('name') or item.get('competitor_name', '')
        country = item.get('country', '')
        country_code = item.get('country_code', '')
        
        # Store unique competitors
        if competitor_id and competitor_id not in competitors:
            competitors[competitor_id] = {
                'competitor_id': competitor_id,
                'name': competitor_name,
                'country': country,
                'country_code': country_code if country_code else country[:3].upper()
            }
        
        # Create ranking record
        ranking_record = {
            'rank_id': idx + 1,
            'competitor_id': competitor_id,
            'rank': item.get('rank', idx + 1),
            'movement': item.get('movement', 0),
            'points': item.get('points', 0),
            'competitions_played': item.get('competitions_played', 0)
        }
        rankings.append(ranking_record)
    
    print(f"Parsed {len(rankings)} rankings and {len(competitors)} unique competitors")
    return rankings, list(competitors.values())

def save_to_csv(rankings, competitors):
    """Saves the parsed data to CSV files"""
    
    rankings_df = pd.DataFrame(rankings)
    competitors_df = pd.DataFrame(competitors)
    
    rankings_df.to_csv('competitor_rankings.csv', index=False)
    competitors_df.to_csv('competitors.csv', index=False)
    
    print("\n Data saved to CSV files:")
    print(f"   - competitor_rankings.csv ({len(rankings)} rows)")
    print(f"   - competitors.csv ({len(competitors)} rows)")
    
    return rankings_df, competitors_df

def preview_data(rankings_df, competitors_df):
    """Display preview of the data"""
    
    print("\n" + "="*60)
    print("DOUBLES RANKINGS DATA PREVIEW")
    print("="*60)
    
    print("\nCompetitors Table Preview (first 10 rows):")
    print(competitors_df.head(10).to_string())
    
    print("\n Competitor Rankings Table Preview (first 10 rows):")
    print(rankings_df.head(10).to_string())
    
    if len(rankings_df) > 0:
        print("\n Quick Statistics:")
        print(f"   - Total Ranked Competitors: {len(rankings_df)}")
        print(f"   - Unique Countries: {competitors_df['country'].nunique()}")
        print(f"   - Top 5 Countries by Competitors:")
        country_counts = competitors_df['country'].value_counts().head(5)
        for country, count in country_counts.items():
            print(f"      • {country}: {count} competitors")
        
        print(f"\n   Top 5 Ranked Competitors:")
        top_5 = rankings_df.nsmallest(5, 'rank')[['rank', 'competitor_id', 'points']]
        for _, row in top_5.iterrows():
            print(f"      • Rank {int(row['rank'])}: {row['competitor_id']} ({int(row['points'])} points)")

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("DOUBLES RANKINGS DATA EXTRACTION")
    print("="*60)
    
    # Step 1: Fetch data
    raw_data = fetch_doubles_rankings()
    
    if raw_data:
        # Step 2: Parse JSON
        rankings, competitors = parse_rankings_data(raw_data)
        
        if rankings and competitors:
            # Step 3: Save to CSV
            rankings_df, competitors_df = save_to_csv(rankings, competitors)
            
            # Step 4: Preview the data
            preview_data(rankings_df, competitors_df)
            
            print("\n" + "="*60)
            print("RANKINGS DATA EXTRACTION COMPLETE!")
            print("="*60)
        else:
            print(" No rankings data found in response")
            print("The API might require different parameters or may not have doubles rankings in trial version")
    else:
        print(" Failed to fetch rankings data")
        print("\nNote: The trial API may not include doubles rankings.")
        print("We can still proceed with competitions and venues data for now.")