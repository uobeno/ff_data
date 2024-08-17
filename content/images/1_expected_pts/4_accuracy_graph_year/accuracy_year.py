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
df = query('image_ep_1_accuracy_graph_year','accuracy_year.sql')
df = df.sort_values(by=['draft_rank', 'year', 'position'])

# Create the line plot
fig = px.line(
    df, 
    x='draft_rank', 
    y='points_scored', 
    color='year', 
    facet_row='position', 
    line_group='year',
    color_discrete_sequence=px.colors.qualitative.Plotly
    )


# Update layout for better readability
fig.update_layout(
    title="Line Plots by Position and Year",
    xaxis_title="Draft Rank",
    yaxis_title="PPR Points / Game",
    height=1200,
    width=1000,
    margin=dict(l=50, r=50, t=100, b=50)
)

# Save the figure
fig.write_image('accuracy_graph_year.png', scale=2)

