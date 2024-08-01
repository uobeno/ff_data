import plotly.express as px
import plotly.io as pio
import pandas as pd

import sys
from pathlib import Path

# Define the path to the styles directory
styles_path = Path(__file__).resolve().parent.parent / 'utils'
# Add the styles directory to sys.path
sys.path.append(str(styles_path.resolve()))

# Import the custom template
from style import custom_template

# Set the custom template as the default
pio.templates.default = custom_template

# Sample data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'Value': [10, 15, 7, 12, 9, 14, 11, 8, 13, 16],
    'Color': [
        '#93F063', '#F8D82F', '#3E3BD0', '#E94126', '#C4E1A6', '#F2E29B',
        '#6F6DCE', '#F5736F', '#F0F0F0', '#333333'
    ]
})

# Create a figure to showcase the color palette
fig = px.bar(data, x='Category', y='Value', color='Color',
             color_discrete_map={color: color for color in data['Color']},
             title='Color Palette Showcase')

fig.update_layout(
    title_text='Color Palette Showcase',
    xaxis_title='Category',
    yaxis_title='Value'
)

fig.show() 

# Save the figure
fig.write_image('color_palette_showcase.png', scale=2, width=1200, height=800)
