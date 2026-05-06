import json


def read_json_to_list(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Convert all values to a list of strings
    string_list = []

    for value in data.values():
        if isinstance(value, list):
            string_list.extend(value)
        else:
            string_list.append(str(value))

    return string_list