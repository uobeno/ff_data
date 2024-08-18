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
df = query('image_hype_high_def','high_hype.sql')

import plotly.express as px

# Create a histogram of pick_hype with facet rows by position
fig = px.histogram(
    df, 
    x="pick_hype", 
    facet_row="position",
    facet_col="rook_flag",
    color="year",  # Optional: Color by position for better differentiation
    title="Distribution of Pick Hype by Position",
    template="plotly_white"
)

# Customize bin size, axis titles, etc. if needed
fig.update_layout(
    xaxis_title="Pick Hype",
    yaxis_title="Number of Players",
    height=1000
)

# Make the y-axis different for each scatter plot
fig.update_yaxes(matches=None)

# Save the figure
fig.write_image('hype_define_percent_hist.png', scale=2)

