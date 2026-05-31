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
    # 1. Start with a clean record list
    if isinstance(data, dict):
        # Handle cases where the data is inside a wrapper key (e.g {"products": [...]})
        list_keys = [k for k, v in data.items() if isinstance(v, list)]
        if list_keys and len(data) <= 4:
            main_data = data[list_keys[0]]
        else:
            main_data = [data]
    else:
        main_data = data

    # 2. Base normalization
    df = pd.json_normalize(main_data)

    # 3. Avoid infinite loops by tracking column states directly
    columns_to_process = list(df.columns)
    
    while columns_to_process:
        col = columns_to_process.pop(0)
        
        # Safety check if the column was dropped in a previous iteration
        if col not in df.columns:
            continue
            
        non_null_vals = df[col].dropna()
        if non_null_vals.empty:
            continue

        # Check for nested dictionaries
        if any(isinstance(val, dict) for val in non_null_vals):
            nested_df = pd.json_normalize(non_null_vals).set_index(non_null_vals.index)
            # Add new sub-columns back into the processing queue
            new_cols = [f"{c}_{col}" for c in nested_df.columns]
            df = df.drop(columns=[col]).join(nested_df, rsuffix=f"_{col}")
            columns_to_process.extend(new_cols)

        # Check for nested lists that are not empty
        elif any(isinstance(val, list) for val in non_null_vals):
            # Check if the list contains dictionaries before exploding.
            first_list = next((v for v in non_null_vals if isinstance(v, list) and v), None)
            
            df = df.explode(col)
            
            # Flatten inner elements if they are dictionaries after explosion.
            if first_list and isinstance(first_list[0], dict):
                columns_to_process.append(col)

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


