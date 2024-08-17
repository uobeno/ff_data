# expected_total.py
import sys
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import statsmodels.api as sm


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
df = query('image_ep_1_accuracy_scatter','accuracy_scatter.sql')

# Sample DataFrame
# df should have columns: position, expected_points, actual_points, year

fig = px.scatter(df, 
                 x='expected_points', 
                 y='actual_points', 
                 color='year', 
                 facet_row='position',
                #  trendline='ols', # Add a trendline
                 title='Actual vs Expected Points by Position and Year',
                 hover_data={'name': True})

# Get the axis limits
df_ranges = query('image_ep_1_accuracy_scatter_axis','accuracy_scatter_axis.sql')

# Get the unique positions (rows) in the facet grid
positions = df['position'].unique()

# Update axis range and add 45-degree line for each row
for position in positions:
    # Filter data for the current position
    row_index = list(positions).index(position) + 1  # 1-based index
    
    # Get the min and max for x and y axes from df_ranges
    range_data = df_ranges[df_ranges['position'] == position].iloc[0]
    x_min, x_max = range_data['min_x'], range_data['max_x']
    y_min, y_max = range_data['min_y'], range_data['max_y']
    
    # Update x and y axis ranges for the current row
    fig.update_xaxes(range=[x_min, x_max], row=row_index, col=1)
    fig.update_yaxes(range=[y_min, y_max], row=row_index, col=1)
    
    # Add a 45-degree line for the current row
    fig.add_trace(go.Scatter(
        x=[x_min, x_max],
        y=[y_min, y_max],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        showlegend=False
    ), row=row_index, col=1)

    df_filtered = df[df['position'] == position]
    
    # Fit regression model
    X = sm.add_constant(df_filtered['expected_points'])
    model = sm.OLS(df_filtered['actual_points'], X).fit()

    # Calculate regression statistics
    r_squared = model.rsquared
    coef = model.params[1]  # Slope coefficient

    # Add regression line
    fig.add_trace(go.Scatter(
        x=df_filtered['expected_points'],
        y=model.predict(X),
        mode='lines',
        name=f'Regression {position}',
        line=dict(dash='dash', color='black'),
        legendgroup='regression'
    ), row=row_index, col=1)

    # Add regression stats as annotation
    fig.add_annotation(
        xref='paper', yref='paper',
        x=range_data['max_x'],
        y=range_data['max_y'],
        text=f'R²: {r_squared:.2f}<br>Slope: {coef:.2f}',
        showarrow=False,
        row=row_index,
        col=1
        )  

# Customize the layout to improve readability
fig.update_layout(
    height=1600,  # Adjust height as needed
    width=600,   # Adjust width as needed
    title_font_size=20,
    margin=dict(l=50, r=50, t=80, b=50),  # Adjust margins
)

# Improve readability of facets and axis labels
fig.update_yaxes(title='Actual Points')
# Update xaxes for all facets to show ticks
fig.update_xaxes(
    showticksuffix='all',  # Show all ticks suffixes
    showticklabels=True,  # Ensure tick labels are shown
    title='Expected Points'
    )

# Save the figure
fig.write_image('accuracy_graph_scatter.png', scale=2)

# fig.show()
# I like to show this one because then people can hover over the data and look at the actual player naem
# which provides way more use and context
