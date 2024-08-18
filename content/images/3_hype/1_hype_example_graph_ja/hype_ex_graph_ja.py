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
df = query('image_ep_3_hype_ex_graph_ja','hype_ex_graph_ja.sql')

# Create a figure
fig = go.Figure()

# Adding bars for each metric, with customized base
metrics = ['prior_year_ppg', 'pick_hype', 'expected_ppg', 'pick_accuracy', 'actual_ppg']
colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
metric_name = {
    'prior_year_ppg': 'prior',
    'pick_hype': 'hype',
    'expected_ppg': 'expected',
    'pick_accuracy': 'accuracy',
    'actual_ppg': 'actual'
    }

for metric, color in zip(metrics, colors):
    name = metric_name[metric]
    # Apply conditional logic for the base of the bar
    if metric == 'pick_hype':
        base = df['prior_year_ppg']
        bar_color = dict(color=df['pick_hype'].apply(lambda x: 'green' if x > 0 else 'red'))
        width=0.08
        offset=0.9
    elif metric == 'pick_accuracy':
        base = df['expected_ppg']
        bar_color = dict(color=df['pick_hype'].apply(lambda x: 'red' if x >= 0 else 'green'))
        width=0.08
        offset=0.9
    else:
        base = 0  # Default base to zero for other metrics
        bar_color = dict(color=df['pick_hype'].apply(lambda x: color if x > 0 else color))
        width=0.15
        offset=0.1

    fig.add_trace(go.Bar(
        x=df['year'],
        y=df[metric],
        base=base,
        name=metric,
        marker=bar_color,
        width=width,
        text=df[metric],
        textposition="outside",
        # texttemplate=f'{name}' + ': <br> %{text}',  # Custom text format
        outsidetextfont=dict(size=8)
        # offset=offset
    ))

# Update layout for grouped bars
fig.update_layout(
    barmode='group',
    title='Josh Allen: Hype and Accuracy vs ADP Expected PPG',
    xaxis_title='Year',
    yaxis_title='Value',
    legend_title='Metrics'
)
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='show')
fig.update_layout(bargap=0.4)
fig.update_layout(bargroupgap=0.4)

# Save the figure
fig.write_image('hype_graph_ja.png', scale=2)

