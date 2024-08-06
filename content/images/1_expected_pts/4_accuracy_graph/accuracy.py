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
df = query('image_ep_1_accuracy_graph','accuracy.sql')

# Create a Plotly Express figure with facet grids
fig = px.bar(
    df,
    x='draft_rank',
    y='expected_ppg',
    color='position',  # Use different colors for positions
    color_discrete_sequence=['#93F063','#E94126','#3E3BD0','#F8D82F'],
    facet_col='position',
    facet_row='year',
    labels={'expected_ppg': 'Expected PPG', 'draft_rank': 'Draft Rank'},
    title='Facet Grid of Bar Charts by Year and Position',
    height=3200,
    width=3200
)

# Define unique values for years and positions
years = sorted(df['year'].unique())
print(years)
positions = sorted(df['position'].unique())
print(positions)

# Add second bar series to each facet using enumerate
for i, year in enumerate(years):
    for j, position in enumerate(positions):
        # Filter the dataframe for the current year and position
        df_filtered = df[(df['position'] == position) & (df['year'] == year)]

        # Add the bars for the second series
        fig.add_trace(go.Bar(
                x=df_filtered['draft_rank'],
                y=df_filtered['abs_pick_accuracy'],
                base=df_filtered['bar_start'],
                name=f'Pick Accuracy ({position}, {year})',
                marker_color=df_filtered['bar_color'],  # Use the color for the position
                showlegend=False,
                text=df_filtered['label'],
                textposition='outside',
                textangle=45
            ),
        row=len(years) - i,  # Row index (1-based)
        col=j + 1   # Column index (1-based)
        )

        fig.add_trace(go.Scatter(
            x=df_filtered['draft_rank'],
            y=df_filtered['name_label'],
            mode='text',
            text=df_filtered['label'],
            textposition='top center',
            showlegend=False
        ), row=len(years) - i, col=j + 1)


# Update layout for better visibility
fig.update_xaxes(matches=None)
fig.update_xaxes(title_text='Draft Rank', showticklabels=True)
fig.update_yaxes(title_text='Expected PPG', showticklabels=True)
fig.update_xaxes(title_text='Draft Rank', row=len(years), col='all')
fig.update_layout(
    barmode='overlay'
)

# Save the figure
fig.write_image('accuracy_graph.png', scale=2)

