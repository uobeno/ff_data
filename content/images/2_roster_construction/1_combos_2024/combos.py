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
df = query('image_roster_1combo_prep_2024','combo_prep.sql')

# Step 1: Create dictionaries from specified columns
df['player_dict'] = df[['name', 'position', 'fppg_ppr', 'round', 'year']].apply(lambda row: row.to_dict(), axis=1)
print('add player dict')
# print(df.head())

# Step 2: Group by 'round' and collect dictionaries into arrays
# You can theoretically only draft 1 player in each round
# So we need to calculate all of those possibilities
grouped = df.groupby(['round', 'year'])['player_dict'].apply(list).reset_index(name='dict_array')
print('create draft round options')
print(grouped.head())

# Step 3: Dump arrays into a single array
# This allows us to feed it into itertools
all_dictionaries = grouped['dict_array'].tolist()
print('dictionaries:')
print(all_dictionaries[2])

# Display the final output
# Preview what a few of the rounds look like
print("\nFinal Array of Dictionary Arrays:")
for i, array in enumerate(all_dictionaries[:2], start=1):
    print(f"Round {i}:")
    for d in array:
        print(d)

# Use itertools.product to generate combinations
combinations = list(itertools.product(*all_dictionaries))

# The number of distinct teams that could be drafted
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

# The number of players we put on a team
print("drafted players: " + str(len(draft_db)))

print('output db sample: ')
draft_db.head()

# Connect to the SQLite database
conn , cur = connect_to_db()

print('Writing to DB')
# Insert data in chunks
draft_db.to_sql('draft_combos_dr10_2024', conn, if_exists='replace', index=False, chunksize=10000)

# Close the connection
conn.close()
print('Done! Closed connection')
