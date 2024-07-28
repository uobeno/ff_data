import sqlite3
from pathlib import Path

import os

# Get the path of the current file we're at
# ff/ff_data/pipeline/processing/data_pipeline.py
# And get to the nfl database here
# ff/ff_data/raw_data/nfl/src_code/nfl.db
base_dir = Path(__file__).parent.parent.parent

# Construct the relative path to the nfl database
db_base = base_dir / "raw_data" / "nfl" / "src_code" / "nfl.db"
db_path = db_base.resolve()

# Function to execute a SQL file
def execute_sql_file(connection, sql_file):
    # print(f"Working on: {sql_file}")
    with open(sql_file, 'r') as file:
        sql_script = file.read()
    connection.executescript(sql_script)
    print(f"Executed: {sql_file}")

# Establish a connection to the database
conn = sqlite3.connect(db_path)
cur = conn.cursor()

adp_base = base_dir / "raw_data" / "adp" / "src_code" / "adp.db"
adp_path = adp_base.resolve()

# Attach the secondary database (adp.db)
attach_sql = f"ATTACH DATABASE '{adp_path}' AS adp_db;"
cur.execute(attach_sql)

# List of SQL files to execute in order
sql_files = [
    "1_adp_prep.sql", #add position and draft pick to adp data
    "1_nfl_enhanced.sql", #add non window stats to nfl data
    "2_clean_names.sql", #create a player name key to join adp and nfl
    "3_player_windows.sql", #add player window stats
    "4_hist_adp_fpts.sql", #add hype / accuracy vs historical adp
    "5_nfl_team_stats.sql" #roll team position groups up to aggregate stats
]

# Map from the current directory to the directory where the sql files live
start_dir = Path(__file__).parent.parent
sql_base = start_dir / "sql"

# Execute each SQL file
for sql_file in [sql_files[5]]:
    file_path = sql_base / sql_file
    execute_sql_file(conn, file_path.resolve())

print("Done processing all sql files")

# Commit the changes and close the connection
conn.commit()
conn.close()

# To run, type this in the terminal: python3 pipeline/processing/data_pipeline.py