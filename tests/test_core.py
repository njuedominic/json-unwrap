import pandas as pd
import pytest
import jsonunwrap as ju

def test_unwrap_data_basic_flattening():
    """Test that basic nested dictionaries are flattened with dot notation."""
    sample = {"id": 1, "user": {"name": "Alice", "role": "Admin"}}
    df = ju.unwrap_data(sample)
    
    assert isinstance(df, pd.DataFrame)
    assert "user.name" in df.columns
    assert df.loc[0, "user.name"] == "Alice"

def test_unwrap_data_list_explosion():
    """Test that lists inside dictionaries are properly exploded into rows."""
    sample = {"id": 101, "hobbies": ["reading", "coding"]}
    df = ju.unwrap_data(sample)
    
    # Should create 2 rows because of the 2 items in the list
    assert len(df) == 2
    assert list(df["hobbies"]) == ["reading", "coding"]
