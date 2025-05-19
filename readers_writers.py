"""
Readers and writers for different formats.
"""
import pandas as pd
from io import StringIO

def read_xvg(filepath):
    # Read the file, skipping metadata lines
    with open(filepath, 'r') as f:
        lines = [line for line in f if not line.startswith(('@', '#'))]

    # Use pandas to read the remaining lines
    data = pd.read_csv(StringIO(''.join(lines)), delim_whitespace=True, header=None)
    return data

def merge_multiple_xvg(list_xvg_paths: list, shared_x_name: str, list_y_names: list):
    full_data = []
    for input_file, density_cat in zip(list_xvg_paths, list_y_names):
        density = read_xvg(input_file)
        density.columns = [shared_x_name, density_cat]
        full_data.append(density)

    merged_df = pd.concat(full_data, axis=1, join="inner")
    merged_df = merged_df.loc[:, ~merged_df.T.duplicated()]
    return merged_df