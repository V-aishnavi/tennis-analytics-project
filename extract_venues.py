import requests
import pandas as pd

API_KEY = "wJU8Lwraqz1Y3xaAvcuw9OIkEX8dAReatoHtWMZe"

def fetch_complexes_data():
    """Fetches complexes and venues data from Sportradar API"""
    
    base_url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"
    params = {'api_key': API_KEY}
    
    try:
        print("Fetching complexes and venues data...")
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f" Successfully fetched data!")
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def parse_complexes_venues_data(data):
    """Parses the JSON data into Complexes and Venues tables"""
    
    complexes = []
    venues = []
    
    if not data or 'complexes' not in data:
        print("No complexes data found")
        return [], []
    
    print(f"\nProcessing {len(data['complexes'])} complexes...")
    
    for complex_obj in data['complexes']:
        complex_id = complex_obj.get('id', '')
        complex_name = complex_obj.get('name', '')
        
        complex_record = {
            'complex_id': complex_id,
            'complex_name': complex_name
        }
        complexes.append(complex_record)
        
        if 'venues' in complex_obj:
            for venue in complex_obj['venues']:
                venue_record = {
                    'venue_id': venue.get('id', ''),
                    'venue_name': venue.get('name', ''),
                    'city_name': venue.get('city', ''),
                    'country_name': venue.get('country', ''),
                    'timezone': venue.get('timezone', ''),
                    'complex_id': complex_id
                }
                venues.append(venue_record)
    
    print(f" Parsed {len(complexes)} complexes and {len(venues)} venues")
    return complexes, venues

def save_to_csv(complexes, venues):
    """Saves the parsed data to CSV files"""
    
    complexes_df = pd.DataFrame(complexes)
    venues_df = pd.DataFrame(venues)
    
    complexes_df.to_csv('complexes.csv', index=False)
    venues_df.to_csv('venues.csv', index=False)
    
    print("\n Data saved to CSV files:")
    print(f"   - complexes.csv ({len(complexes)} rows)")
    print(f"   - venues.csv ({len(venues)} rows)")
    
    return complexes_df, venues_df

def preview_data(complexes_df, venues_df):
    """Display preview of the data"""
    
    print("\n" + "="*60)
    print("COMPLEXES & VENUES DATA PREVIEW")
    print("="*60)
    
    print("\n Complexes Table Preview (first 10 rows):")
    print(complexes_df.head(10).to_string())
    
    print("\n Venues Table Preview (first 10 rows):")
    print(venues_df.head(10).to_string())
    
    print("\n Quick Statistics:")
    print(f"   - Total Complexes: {len(complexes_df)}")
    print(f"   - Total Venues: {len(venues_df)}")
    
    if len(venues_df) > 0 and 'country_name' in venues_df.columns:
        # Count venues by country (excluding empty)
        country_counts = venues_df[venues_df['country_name'] != '']['country_name'].value_counts().head(5)
        if len(country_counts) > 0:
            print(f"\n   Top 5 countries by venues:")
            for country, count in country_counts.items():
                print(f"      • {country}: {count} venues")
    
    if len(venues_df) > 0 and 'complex_id' in venues_df.columns:
        # Find complexes with multiple venues
        venues_per_complex = venues_df.groupby('complex_id').size()
        multi_venue = venues_per_complex[venues_per_complex > 1]
        if len(multi_venue) > 0:
            print(f"\n   Complexes with multiple venues: {len(multi_venue)} complexes")
            # Show top 5
            top_multi = multi_venue.head(5)
            for complex_id, count in top_multi.items():
                # Get complex name
                complex_name = complexes_df[complexes_df['complex_id'] == complex_id]['complex_name'].values
                if len(complex_name) > 0:
                    print(f"      • {complex_name[0]}: {count} venues")

if __name__ == "__main__":
    print("="*60)
    print("TENNIS VENUES & COMPLEXES DATA EXTRACTION")
    print("="*60)
    
    raw_data = fetch_complexes_data()
    
    if raw_data:
        complexes, venues = parse_complexes_venues_data(raw_data)
        complexes_df, venues_df = save_to_csv(complexes, venues)
        preview_data(complexes_df, venues_df)
        
        print("\n" + "="*60)
        print(" VENUES & COMPLEXES DATA EXTRACTION COMPLETE!")
        print("="*60)
    else:
        print(" Failed to fetch complexes data")