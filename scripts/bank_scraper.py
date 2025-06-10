"""
Google Play Store Review Scraper for Ethiopian Banking Apps
Fetches user reviews for CBE, BOA, and Dashen Bank mobile apps.
"""

import pandas as pd
from google_play_scraper import app, reviews, Sort
from tqdm import tqdm  # For progress bars
import time
import os

# Configuration
BANK_APPS = {
    "cbe": "com.combanketh.mobilebanking",
    "boa": "com.boa.boaMobileBanking",
    "dashen": "com.dashen.dashensuperapp"
}

# Output directory
RAW_DATA_DIR = "../data/raw"

os.makedirs(RAW_DATA_DIR, exist_ok=True)

def fetch_app_info(app_id):
    """Get basic app metadata (name, installs, version)"""
    try:
        app_data = app(app_id)
        return {
            'app_name': app_data.get('title', ''),
            'installs': app_data.get('installs', ''),
            'version': app_data.get('version', '')
        }
    except Exception as e:
        print(f"Error fetching app info for {app_id}: {str(e)}")
        return None

def scrape_reviews(app_id, bank_name, max_reviews=700):
    """
    Scrape reviews with pagination and error handling
    Returns: DataFrame with reviews
    """
    all_reviews = []
    continuation_token = None
    
    with tqdm(total=max_reviews, desc=f"Scraping {bank_name}") as pbar:
        while len(all_reviews) < max_reviews:
            try:
                batch, continuation_token = reviews(
                    app_id,
                    lang='en',          # English reviews
                    country='et',       # Ethiopia
                    sort=Sort.NEWEST,   # Get newest first
                    count=100,          # Max per batch
                    continuation_token=continuation_token
                )
                
                if not batch:
                    break
                
                all_reviews.extend(batch)
                pbar.update(len(batch))
                
                # Avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"Error scraping {bank_name}: {str(e)}")
                time.sleep(10)  # Longer wait if error
                continue
    
    return pd.DataFrame(all_reviews[:max_reviews])

def save_reviews(df, bank_name):
    """Save reviews to CSV with timestamp"""
    timestamp = pd.Timestamp.now().strftime("%Y%m%d")
    filename = f"{RAW_DATA_DIR}/{bank_name}_reviews_{timestamp}.csv"
    # Ensure the directory exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} reviews to {filename}")
    return filename

def main():
    """Main scraping workflow"""
    all_data = []
    
    for bank_name, app_id in BANK_APPS.items():
        # Get app metadata
        app_info = fetch_app_info(app_id)
        
        # Scrape reviews
        reviews_df = scrape_reviews(app_id, bank_name)
        
        if reviews_df.empty:
            continue
            
        # Add metadata columns
        reviews_df['bank'] = bank_name.upper()
        if app_info:
            for key, value in app_info.items():
                reviews_df[key] = value
        
        # Save to CSV
        save_reviews(reviews_df, bank_name)
        all_data.append(reviews_df)
    
    # Combine all bank data
    if all_data:
        full_df = pd.concat(all_data)
        master_file = f"{RAW_DATA_DIR}/all_reviews_combined.csv"
        full_df.to_csv(master_file, index=False)
        print(f"\nFinal combined data saved to {master_file}")
        print(f"Total reviews collected: {len(full_df)}")
    else:
        print("No reviews were scraped successfully.")

if __name__ == "__main__":
    main()