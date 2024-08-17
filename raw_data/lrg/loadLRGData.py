import os
import pandas as pd
from pathlib import Path

# Map to the base directory, we'll use this to get to every file
base_dir = Path(__file__).parent.parent.parent #Should be /ff_data

# ff_data/
# Add the path to the query utility
util_path = base_dir / 'content' / 'images' / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(util_path.resolve()))

# Import the connection from the utils path
from query import connect_to_db

# Path to the CSV that we want to import into our database
csv = base_dir / 'db_output' / 'private_csv' / 'lrg.csv'
csv_path = csv.resolve()

conn, cur = connect_to_db()

# # Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# # Add the year column to the DataFrame
df['Year'] = year

# # Save the DataFrame to the SQL database
df.to_sql('nfl_results', engine, if_exists='append', index=False)

print("Data has been successfully saved to the SQL database.")
