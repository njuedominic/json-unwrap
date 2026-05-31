# jsonunwrap

**jsonunwrap** is a simple JSON flattening and normalization library.

```python
>>> import jsonunwrap as ju
>>> url = "https://dummyjson.com/carts"
>>> fetchdata = ju.fetch_json(url)
>>> df = ju.unwrap_data(fetchdata)
>>> df.columns
Index(['id', 'user.name', 'hobbies'], dtype='object')
>>> len(df)
2
```

jsonunwrap allows you to deeply normalize complex, semi-structured nested JSON data into clean pandas DataFrames extremely easily.

---

## Installing jsonunwrap

jsonunwrap is available on PyPI:

```bash
$ python -m pip install jsonunwrap
```

## Supported Features & Best–Practices

jsonunwrap is ready for the data parsing demands of modern web APIs, automation scripts, and data engineering pipelines.

- Recursive Deep-Flattening (Dot-notation formatting for sub-dictionaries)
- Automated List Explosion (Spanning embedded primitive lists safely into unique rows)
- Endpoint Target Binding (Fetch and write stream sequences in a single wrapper)
- Clean API Namespace (Unified module boundaries with zero complex configuration maps)

---

## Quick Usage Reference

### Download, Normalize, and Export an API Stream to Disk

```python
import jsonunwrap as ju

target_url = "url"
output_file = "data/normalized_users.csv"

# Fetch, unwrap nested schemas, and generate a local CSV payload
df = ju.json_to_csv(target_url, output_file)
```

---

## Core API Documentation

The complete package interaction map exposes three primary interfaces:

### `jsonunwrap.unwrap_data(data)`
Recursively flattens an in-memory dictionary or list of records. Returns a parsed `pandas.DataFrame`.

### `jsonunwrap.fetch_json(url, **kwargs)`
A connection delivery utility utilizing the `requests` transport subsystem. Passes `**kwargs` onwards to target handlers.

### `jsonunwrap.json_to_csv(url, output_path)`
High-level workflow coordinator connecting remote schema acquisition loops directly to a structural local CSV export.

---

## Contributions & Testing

To test modifications locally or prepare adjustments, execute using `pytest`:

```bash
\$ git clone https://github.com/njuedominic/json-unwrap
\$ cd jsonunwrap
\(python -m pip install -e .[test]\) pytest
```
