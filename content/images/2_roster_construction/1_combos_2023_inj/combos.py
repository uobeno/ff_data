# expected_total.py
import sys
from pathlib import Path
import pandas as pd
import itertools
import sqlite3

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from query import query, connect_to_db

# Get data for our query
df = query('image_roster_1combo_prep','combo_prep.sql')

# Step 1: Create dictionaries from specified columns
df['player_dict'] = df[['name', 'position', 'games', 'fppg_ppr', 'round', 'year']].apply(lambda row: row.to_dict(), axis=1)
print('add player dict')
# print(df.head())

# Step 2: Group by 'round' and collect dictionaries into arrays
grouped = df.groupby(['round', 'year'])['player_dict'].apply(list).reset_index(name='dict_array')
print('create draft round options')
print(grouped.head())

# Step 3: Dump arrays into a single array
all_dictionaries = grouped['dict_array'].tolist()
# This list looks like [
# Round 1:
    # [{'name': 'christian mccaffrey', 'position': 'RB', 'fppg_ppr': 26.09, 'round': '1', 'year': '2024'}
    # {'name': 'ceedee lamb', 'position': 'WR', 'fppg_ppr': 23.2, 'round': '1', 'year': '2024'}]
# Round 2:
    # [{'name': 'brock purdy', 'position': 'QB', 'fppg_ppr': 18.54, 'round': '10', 'year': '2024'}
    # {'name': 'tony pollard', 'position': 'RB', 'fppg_ppr': 11.32, 'round': '10', 'year': '2024'}
    # {'name': 'david njoku', 'position': 'TE', 'fppg_ppr': 10.51, 'round': '10', 'year': '2024'}
    # {'name': 'ladd mcconkey', 'position': 'WR', 'fppg_ppr': 11.22, 'round': '10', 'year': '2024'}]
# ]

"""
Outline:

Generate 100,000 combos (5 round chunks)
    - all_dictionaries[0:4]
    - all_dictionaries[5:9]
    - all_dictionaries[10:15]

The function needs to take in a list of dictionaries,
generate chunks -> write to a table
disqualify chunks -> write to a new table

Then we can start from the top again and cross join the tables or we can

"""

# Use itertools.product to generate combinations
combinations = list(itertools.product(*all_dictionaries))

print('made combos: ' + str(len(combinations)))

# Display the combinations
print("\nCombinations of Dictionaries:")
for combination in combinations[:5]:
    print(combination)

# Let's put the combinations into a pandas dataframe
# Flatten combinations into a list of dictionaries with team_id
players_list = []
for team_id, team in enumerate(combinations, start=1):
    for player in team:
        player_with_team = player.copy()
        player_with_team['team_id'] = team_id
        players_list.append(player_with_team)

# Create a DataFrame from the list of dictionaries
draft_db = pd.DataFrame(players_list)

print("drafted players: " + str(len(draft_db)))

print('output db sample: ')
draft_db.head()

# Connect to the SQLite database
conn , cur = connect_to_db()

print('Writing to DB')
# Insert data in chunks
draft_db.to_sql('draft_combos_dr10', conn, if_exists='replace', index=False, chunksize=10000)

# Close the connection
conn.close()
print('Done! Closed connection')
