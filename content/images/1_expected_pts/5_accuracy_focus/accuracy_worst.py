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
df = query('image_ep_1_accuracy_graph_focus2','accuracy_focus.sql')
df = df.sort_values(by='expected_ppg', ascending=True)

# Define the color mapping for positions
position_color_map = {
    'RB': '#E94126',  # Red for RB
    'QB': '#93F063',  # Green for QB
    'TE': '#3E3BD0',  # Blue for TE
    'WR': '#F8D82F'   # Yellow for WR
}

# Create a stacked horizontal bar chart
fig = go.Figure()

# First series (base of the bar)
fig.add_trace(go.Bar(
    x=df['bar_start'],  # Starting value for the bar
    y=df['name'],  # Bar per player
    orientation='h',  # Horizontal bar chart
    marker_color=[position_color_map[pos] for pos in df['position']],  # Base color depends on position
    name='Position',  # Name for the legend
    showlegend=True
))

# Second series (stacked on top of the base)
fig.add_trace(go.Bar(
    x=df['abs_pick_accuracy'],  # Height of the stacked bar
    y=df['name'],  # Bar per player
    orientation='h',  # Horizontal bar chart
    marker_color=df['bar_color'],  # Stacked bar colors from "bar_color" column
    name='Pick Accuracy',  # Name for the legend
    text=df['label'],  # Labels from "label" column
    textposition='outside',  # Positioning the text on the bars
    textfont_size=20,  # Set font size with a dict
    showlegend=True
))

fig.update_yaxes(showticklabels=False)

# Update layout to stack bars
fig.update_layout(
    title="Fantasy graveyard, the least accurate we've",
    xaxis_title="Value",
    yaxis_title="Player",
    barmode='stack',  # Enables stacked bars
    height=600,
    width=1200
)

# Save the figure
fig.write_image('accuracy_worst.png', scale=2)