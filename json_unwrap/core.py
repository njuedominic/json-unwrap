"""
This module contains the core functionality for the json_unwrap package.
The main function is `json_to_csv`, which converts a JSON file to a CSV file.
"""
import os
from typing import Any, Dict, List, Union
import pandas as pd
import requests

def unrwap_data(data: Union[Dict[str, Any], List[Any]], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Takes a nested JSON object and flattens it into a single level dictionary.
    
    Args:
        data: The JSON data to be unwrapped, which can be a dictionary or a list.
        parent_key: The base key to use for the current level of nesting (used for recursion).
        sep: The separator to use between keys when flattening.

    Returns:
        A flattened dictionary with unwrapped keys.

    """
    #. 1 Input validation
    if isinstance(data, dict):
        main_data = next(
            (value for value in data.values() if isinstance(value, list)),
            [data]
        )
    else:
        main_data = data


    #2. Normalize the JSON data using pandas
    df = pd.json_normalize(main_data)

   # Flatten the nested columns and use a while loop to handle deeply nested structures
    changed = True
    while changed:
        changed = False
        for col in list(df.columns):
            # Explode lists
            if any(isinstance(val, list) for val in df[col].dropna()):
                df = df.explode(col)
                changed = True
                break  # Break to refresh columns list after structural change

            # Normalize and join dictionaries
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
    df = unrwap_data(raw_data)
    
    df.to_csv(output_path, index=False)
    return df


