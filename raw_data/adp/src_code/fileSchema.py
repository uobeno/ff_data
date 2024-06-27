import os
import pandas as pd

# Define the directory containing your CSV files
csv_directory = '/Users/beoconno/documents/ff/raw_data/adp/csv'

# Initialize a variable to hold the common columns
common_columns = None

# Loop through each file in the directory
for filename in sorted(os.listdir(csv_directory)):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(csv_directory, filename)
        
        # Read the first line of the CSV file
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            columns = first_line.split(',')
            second_line = file.readline().strip()
        
        # If this is the first file, initialize common_columns
        if common_columns is None:
            common_columns = set(columns)
        else:
            # Find the intersection with the current file's columns
            common_columns.intersection_update(columns)
            
        # Print the filename and the first line
        print(f"File: {filename}")
        print(f"First Line: {first_line}")
        # print(f"Second Line: {second_line}\n")

for column in common_columns:
    print(column)