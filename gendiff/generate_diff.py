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


def generate_diff(path_1, path_2, format_name='stylish'):
    file_1_format = path_1.split('.')[-1]
    file_2_format = path_2.split('.')[-1]
    with open(path_1) as file_1:
        data_1 = parse(file_1, file_1_format)
    with open(path_2) as file_2:
        data_2 = parse(file_2, file_2_format)

    diffs = build_diff(data_1, data_2)

    formatter = get_formatter(format_name)
    formated_diffs = formatter(diffs)

    return formated_diffs
