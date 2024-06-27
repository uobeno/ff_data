import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

# Get the path of the current file
script_dir = Path(__file__).parent #Should be /src_code

# Construct the relative path to the CSV file
csv_dir_path = script_dir / '..' / 'csv'
csv_directory = csv_dir_path.resolve()

# Get a sorted list of CSV files in the directory
file_list = sorted([f for f in os.listdir(csv_directory) if f.endswith('.csv')])
print(file_list)

# Create a SQLite database (or connect to an existing one)
engine = create_engine(f'sqlite:///{script_dir}/nfl.db')

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Optional: Drop all existing tables so that we load them new
Base = declarative_base()
Base.metadata.drop_all(engine)

# Close the session
session.close()

# Loop through each file in the directory
for filename in file_list:
    # Extract the year from the filename (assuming the year is part of the filename)
    year = filename.split('_')[1].split('.')[0]  # Adjust this according to your filename pattern
    print(year)

    # Construct the full file path
    file_path = os.path.join(csv_directory, filename)
    
    # # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # # Add the year column to the DataFrame
    df['Year'] = year
    
    # # Save the DataFrame to the SQL database
    df.to_sql('nfl_results', engine, if_exists='append', index=False)

print("Data has been successfully saved to the SQL database.")
