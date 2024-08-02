import sqlite3
from pathlib import Path
import pandas as pd

def connect_to_db():
    # This file currently lives at:
    # ff_data/content/images/utils/query.py

    # And get to the nfl database here
    # ff_data/raw_data/nfl/src_code/nfl.db
    base_dir = Path(__file__).parent.parent.parent.parent

    # Construct the relative path to the nfl database
    db_base = base_dir / "db_output" / "nfl.db"
    db_path = db_base.resolve()

    print(f"Connecting to the db at: {db_path}")

    # Establish a connection to the database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Path to the ADP database
    adp_base = base_dir / "db_output" / "adp.db"
    adp_path = adp_base.resolve()
    # Attach the secondary database (adp.db)
    attach_sql = f"ATTACH DATABASE '{adp_path}' AS adp_db;"
    cur.execute(attach_sql)
    return conn, cur

def query(table_name, sql_file_path):
    executing_from = Path(__file__).resolve
    print(f"Execuging from: {executing_from}")

    # Connect to the SQLite database
    conn , cur = connect_to_db()
    
    try:
        # Read the SQL file
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()

        # Prepare the query with DROP and CREATE TABLE
        query_starter = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} AS
        """

        # Combine the query starter with the SQL content
        full_query = query_starter + sql_content

        print(f"Executing {sql_file_path} for {table_name}")

        # Execute the combined query
        cur.executescript(full_query)

        # Commit the transaction
        conn.commit()

        print(f"Done, returning the results")

        # Fetch the results from the newly created table
        query_select = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query_select, conn)

        return df
    finally:
        # Ensure the connection is closed
        conn.close()
