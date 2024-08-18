# expected_total.py
import sys
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from style import custom_template, color_palette
# Import the custom template
from query import query

# Set the custom template as the default
pio.templates.default = custom_template

# Get data for our query
df = query('image_hype_high_def_hist','high_hype.sql')

# Create the facet grid structure
fig = px.scatter(
    df, 
    x="expected_ppg", 
    y="pick_hype", 
    color="year", 
    symbol="rook_flag", 
    facet_row="position"
)

# Customize the layout and other settings as needed
fig.update_layout(
    title="Hype percentage by Position and Rookie vs Regular",
    xaxis_title="Expected PPG",
    yaxis_title="Pick Hype",
    legend_title="Rookie Flag",
    template="plotly_white",
    height=1600  # Adjust height as needed
)

# Make the axes independent
fig.update_xaxes(matches=None)
fig.update_yaxes(matches=None)

# Save the figure
fig.write_image('hype_define_percent_scatter.png', scale=2)

