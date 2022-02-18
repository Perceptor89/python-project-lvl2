import os
from collections import OrderedDict
from gendiff.parser import parse
from gendiff.formatters.get_formatter import get_formatter


def build_diff(data_1, data_2):
    diffs = {}

    added_keys = list(data_2.keys() - data_1.keys())
    removed_keys = list(data_1.keys() - data_2.keys())
    common_keys = list(data_1.keys() & data_2.keys())

    for key in added_keys:
        diffs[key] = {
            'status': 'added',
            'diff': data_2.get(key),
        }

    for key in removed_keys:
        diffs[key] = {
            'status': 'removed',
            'diff': data_1.get(key),
        }

    for key in common_keys:
        value_1 = data_1.get(key)
        value_2 = data_2.get(key)
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            diffs[key] = {
                'status': 'nested',
                'diff': build_diff(value_1, value_2),
            }
        elif value_1 == value_2:
            diffs[key] = {
                'status': 'unchanged',
                'diff': value_1,
            }
        else:
            diffs[key] = {
                'status': 'changed',
                'diff': {
                    'old_value': value_1,
                    'new_value': value_2,
                },
            }

    return OrderedDict(sorted(diffs.items()))


def get_file_data(path):
    file_name, file_extension = os.path.splitext(path)
    with open(path) as file:
        parsed_data = parse(file, file_extension)
    return parsed_data


def generate_diff(path_1, path_2, format_name='stylish'):
    data_1 = get_file_data(path_1)
    data_2 = get_file_data(path_2)

    diffs = build_diff(data_1, data_2)

    formatter = get_formatter(format_name)
    formated_diffs = formatter(diffs)

    return formated_diffs
