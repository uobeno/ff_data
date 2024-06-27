import pandas as pd
from pathlib import Path
from tabulate import tabulate

def csv_to_markdown_file(csv_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file, quotechar='"')
    
    # Convert the DataFrame to a Markdown table
    markdown_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
    
    # Write the Markdown table to the output file
    with open(output_file, 'w') as output:
        output.write(markdown_table)

# Get the path of the current file
script_dir = Path(__file__).parent #Should be /src_code

# Construct the relative path to the CSV file
csv_path = script_dir / '..' / 'src_code' / 'rawDataDict.csv'
output_path = script_dir / '..' / 'src_code' / 'autoDataDict.md'

csv_file = csv_path.resolve()
output_file = output_path.resolve()
csv_to_markdown_file(csv_file, output_file)
