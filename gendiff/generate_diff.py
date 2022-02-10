from collections import OrderedDict
from gendiff.parser import parse_file
from gendiff.formatters.get_formatter import get_formatter


def get_diffs_dict(file_1_data, file_2_data):
    diffs = {}

    added_keys = list(file_2_data.keys() - file_1_data.keys())
    removed_keys = list(file_1_data.keys() - file_2_data.keys())
    common_keys = list(file_1_data.keys() & file_2_data.keys())

    for key in added_keys:
        diffs[key] = {
            'status': 'added',
            'diff': file_2_data.get(key),
        }

    for key in removed_keys:
        diffs[key] = {
            'status': 'removed',
            'diff': file_1_data.get(key),
        }

    for key in common_keys:
        value_1 = file_1_data.get(key)
        value_2 = file_2_data.get(key)
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            diffs[key] = {
                'status': 'nested',
                'diff': get_diffs_dict(value_1, value_2),
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


def generate_diff(path_1, path_2, format_name='stylish'):
    file_1_data = parse_file(path_1)
    file_2_data = parse_file(path_2)

    diffs_dict = get_diffs_dict(file_1_data, file_2_data)

    formatter = get_formatter(format_name)
    formated_diffs = formatter(diffs_dict)

    return formated_diffs
