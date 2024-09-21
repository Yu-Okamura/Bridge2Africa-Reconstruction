"""
Compatible with Python 3.12
Last MOD: 4/10/2024

Updated by Yu Okamura
Please contact yokamura@asu.edu for errors.
"""

import json

def read_json(filename='data.json'):
    """
    Reads a JSON file and returns the parsed data.
    :param filename: Name of the JSON file to read.
    :return: Parsed data from the JSON file, or None if an error occurs.
    """
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return None

def read_shortcut(filename='shortcuts.json'):
    """
    Reads shortcuts from a JSON file and returns the parsed data.
    :param filename: Name of the JSON file to read.
    :return: Parsed data from the JSON file.
    """
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return {}

def write_json(data, filename='shortcuts.json'):
    """
    Writes data to a JSON file.
    :param data: Data to write to the file.
    :param filename: Name of the JSON file to write to.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully written to {filename}")
    except IOError as e:
        print(f"Error writing to {filename}: {e}")
