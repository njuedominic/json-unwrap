"""
This module contains the core functionality for the json_unwrap package.
The main function is `json_to_csv`, which converts a JSON file to a CSV file.
"""
import os
from typing import Any, Dict, List, Union
import pandas as pd
import requests

def unwrap_data(data: Union[Dict[str, Any], List[Any]]) -> pd.DataFrame:
    """
    Normalizes and deeply flattens semi-structured JSON data into a pandas DataFrame.
    """
    # Simply convert a single dictionary into a list containing that dictionary
    if isinstance(data, dict):
        main_data = [data]
    else:
        main_data = data

    # Perform the initial normalization
    df = pd.json_normalize(main_data)

    # Automatically iterate through the columns and deeply flatten any nested structures
    changed = True
    while changed:
        changed = False
        for col in list(df.columns):
            # Explode lists
            if any(isinstance(val, list) for val in df[col].dropna()):
                df = df.explode(col)
                changed = True
                break  # Refresh columns list after structural changes

            # Normalize and merge nested dictionaries
            if any(isinstance(val, dict) for val in df[col].dropna()):
                nested_df = pd.json_normalize(df[col]).set_index(df.index)
                df = df.drop(columns=[col]).join(nested_df, rsuffix=f"_{col}")
                changed = True
                break
                
    return df

 
def fetch_json(url: str, **kwargs: Any) -> Union[Dict[str, Any], List[Any]]:
    """
    Fetches raw JSON data from a URL.
    
    Args:
        url: The endpoint web target.
        **kwargs: Additional arguments passed directly to requests.get (e.g., headers, auth).
    """
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.json()


def json_to_csv(url: str, output_path: str) -> pd.DataFrame:
    """
    Fetches JSON from a URL, deeply flattens it, and saves it directly to a CSV file.
    
    Args:
        url: The endpoint URL containing the target JSON data.
        output_path: Target filesystem path where the CSV will be written.
        
    Returns:
        The generated pandas DataFrame.
    """
    # Ensure the parent output directory exists safely
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    raw_data = fetch_json(url)
    df = unwrap_data(raw_data)
    
    df.to_csv(output_path, index=False)
    return df


