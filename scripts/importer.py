
import pandas as pd
import os
# function to import reviews from a CSV file and return a DataFrame
def import_reviews(csv_file):
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return pd.DataFrame()  # Return empty DataFrame if file not found
    return pd.read_csv(csv_file)