import plotly.graph_objects as go

"""
Late round green QB: #93F063
Late round yellow WR: #F8D82F
Late round blue TE: #3E3BD0
Late round red RB: #E94126

Supporting Colors:
Light Gray: #F0F0F0 (for backgrounds)
Dark Gray: #333333 (for text)

Shades and Variations:
Light Green Variants: #C4E1A6 (lighter), #72C03D (darker)
Yellow Variants: #F2E29B (lighter), #D9B832 (darker)
Blue Variants: #6F6DCE (lighter), #2D2AB3 (darker)
Red Variants: #F5736F (lighter), #D6301F (darker)

"""

# Define the color palette
color_palette = [
    '#93F063',  # Light Green
    '#F8D82F',  # Yellow
    '#3E3BD0',  # Blue
    '#E94126',  # Red
    '#C4E1A6',  # Light Green Variant
    '#F2E29B',  # Yellow Variant
    '#6F6DCE',  # Blue Variant
    '#F5736F',  # Red Variant
    '#F0F0F0',  # Light Gray (Background)
    '#333333'   # Dark Gray (Text)
]

# Define your custom template
custom_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family='Roboto Condensed, sans-serif', size=14, color='#333333'),
        title=dict(font=dict(size=20, color='#333333', family='Roboto Condensed, sans-serif')),
        paper_bgcolor='#F0F0F0',
        plot_bgcolor='#FFFFFF',
        xaxis=dict(
            title=dict(font=dict(size=16, color='#333333', family='Roboto Condensed, sans-serif')),
            tickfont=dict(size=14, color='#333333', family='Roboto Condensed, sans-serif'),
            gridcolor='#E0E0E0'
        ),
        yaxis=dict(
            title=dict(font=dict(size=16, color='#333333', family='Roboto Condensed, sans-serif')),
            tickfont=dict(size=14, color='#333333', family='Roboto Condensed, sans-serif'),
            gridcolor='#E0E0E0'
        ),
        colorway=color_palette
    )
)
