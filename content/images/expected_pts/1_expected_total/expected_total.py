# expected_total.py
import sys
from pathlib import Path
import pandas as pd
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from style import custom_template
# Import the custom template
from query import query

# Set the custom template as the default
pio.templates.default = custom_template

# Get data for our query
df = query('image_ep_1_etotal','expected_total.sql')

# Print a preview of the data into the logs
print(df.head())

# Create the line plot
fig = px.line(df, x='rank', y='avg_ppr_ppg', color='position', 
              title='Average PPR Points per Game by Rank and Position',
              color_discrete_map={
                  'QB': '#93F063',
                  'WR': '#F8D82F',
                  'TE': '#3E3BD0',
                  'RB': '#E94126'
              },
              markers=True)

# Customize layout (optional)
fig.update_layout(
    xaxis_title='Rank',
    yaxis_title='Average PPR Points per Game',
    legend_title='Position'
    # font=dict(family='Arial, sans-serif', size=14, color='#333333')
)

# Save the figure
fig.write_image('expected_total.png', scale=2, width=1200, height=800)
