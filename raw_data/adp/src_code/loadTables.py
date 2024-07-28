import os
import pandas as pd
from sqlalchemy import create_engine
import os

# Define the directory containing your CSV files
csv_directory = '/Users/beoconno/Documents/ff/ff_data/raw_data/adp/csv'

# Get a sorted list of CSV files in the directory
file_list = sorted([f for f in os.listdir(csv_directory) if f.endswith('.csv')])

# Create a SQLite database (or connect to an existing one)
engine = create_engine('sqlite:///adp.db')

# Columns to select from each CSV file
columns_to_select = ["Bye", "AVG", "Rank", "Team", "POS", "Player"]

# Loop through each file in the directory
for filename in file_list:
    # Extract the year from the filename (assuming the year is part of the filename)
    year = filename.split('_')[1]  # Adjust this according to your filename pattern
    print(year)

    # Construct the full file path
    file_path = os.path.join(csv_directory, filename)

    # Read the CSV data
    with open(file_path, 'r') as file:
        # Replace the escape sequence in the file content like "Le","","'Veon Bell"
        processed_data = file.read().replace('","","\'', '')

    # Use StringIO to simulate file reading
    from io import StringIO
    data_io = StringIO(processed_data)
    
    # # Read the CSV file into a DataFrame
    df = pd.read_csv(data_io, usecols=columns_to_select)
    
    # # Add the year column to the DataFrame
    df['Year'] = year
    
    # # Save the DataFrame to the SQL database
    df.to_sql('historical_adp', engine, if_exists='append', index=False)

print("Data has been successfully saved to the SQL database.")
