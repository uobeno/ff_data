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
df = query('image_ep_1_drop','expected_drop.sql')

# Create a Plotly Table dynamically
table_fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                align='center',
                font=dict(color='white'),
                height=40,
                fill_color=color_palette[9]),
    cells=dict(values=[df[col] for col in df.columns],
               align='left',
               fill_color=[
                    ["lightgrey" if i % 2 == 0 else "white" for i in range(len(df))]
                ],
                height=30
                )
        )
    ])

# Add a title to the table
table_fig.update_layout(
    title_text="Expected PPR PPG drop off from #1 finish to #20 finish",
    title_x=0.5,  # Center the title
    title_font=dict(size=18, color="black")
)

table_fig.update_layout(
    margin=dict(l=10, r=10, t=60, b=10),  # Reduce left, right, top, and bottom margins
)

table_fig.update_layout(
    width=500,  # Set width to fit content
    height=250  # Set height to fit content
)

# Save the figure
table_fig.write_image('expected_drop.png', scale=2, width=500, height=250)

