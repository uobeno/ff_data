# expected_total.py
import sys
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

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
df = query('image_ep_1_accuracy_ex_graph','accuracy_ex.sql')

# Create the figure
fig = go.Figure()

# First bar series: regular bar chart with expected_ppg
fig.add_trace(go.Bar(
    x=df['year'],
    y=df['expected_ppg'],
    name='Expected PPG',
    marker_color=color_palette[6]
))

# Second bar series: starts at bar_start with height of abs_pick_accuracy
fig.add_trace(go.Bar(
    x=df['year'],
    y=df['abs_pick_accuracy'],
    base=df['bar_start'],
    name='Pick Accuracy',
    marker_color=df['bar_color']
))

# Additional trace for middle labels
fig.add_trace(go.Scatter(
    x=df['year'],
    y=df['bar_start'] + df['abs_pick_accuracy'] / 2,  # Position text in the middle
    mode='text',
    text=df['pick_accuracy'],
    textposition='middle center',
    showlegend=False  # Hide legend for text labels
))

# Additional trace for expected ppg
fig.add_trace(go.Scatter(
    x=df['year'],
    y=df['expected_ppg'],  # Position text at the top
    mode='text',
    text=[f'exp: {exp}' for exp in df['expected_ppg']],
    textposition='top center',
    showlegend=False  # Hide legend for text labels
))

# Additional trace for actual ppg
fig.add_trace(go.Scatter(
    x=df['year'],
    y=df['actual_ppg'],  # Position text at the top
    mode='text',
    text=[f'act: {act}' for act in df['actual_ppg']],
    textposition='bottom center',
    showlegend=False  # Hide legend for text labels
))

# Update layout
fig.update_layout(
    title='Comparison of Expected PPG and Pick Accuracy',
    xaxis_title='Year',
    yaxis_title='Points',
    barmode='overlay'
)

# Save the figure
fig.write_image('accuracy_ex_graph.png', scale=2)

