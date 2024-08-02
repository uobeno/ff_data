import sys
import plotly.io as pio
from pathlib import Path
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from style import custom_template

# Set the custom template as the default
pio.templates.default = custom_template

# Sample data
data = pd.DataFrame({'x': range(10), 'y1': range(10), 'y2': [x**2 for x in range(10)]})

# Create a subplot figure with 1 row and 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=('Line Plot', 'Scatter Plot'))

# Line plot in the first subplot
fig.add_trace(go.Scatter(x=data['x'], y=data['y1'], mode='lines+markers', name='Line Plot'), row=1, col=1)

# Scatter plot in the second subplot
fig.add_trace(go.Scatter(x=data['x'], y=data['y2'], mode='markers', name='Scatter Plot'), row=1, col=2)

# Update layout
fig.update_layout(title='Plotly Plot Grid', height=400, width=800)

# Save and show the figure
fig.write_image('plotly_grid.png')

fig.show()