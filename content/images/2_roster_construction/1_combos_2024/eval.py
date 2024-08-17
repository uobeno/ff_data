# expected_total.py
import sys
from pathlib import Path
import pandas as pd

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from query import query

# Get data for our query
df = query('image_roster_1combo_eval_2024','eval.sql')
