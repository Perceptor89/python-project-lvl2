import json
from collections import OrderedDict


def to_str(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)


def stylish_formatter(diff_dict):
    lines = []
    for key, diffs in diff_dict.items():
        status = diffs.get('status')
        diff = diffs.get('diff')
        if status == 'changed':
            old_value = diff.get('old_value')
            new_value = diff.get('new_value')
            lines.extend([
                '{0}{1}: {2}'.format('  - ', key, to_str(old_value)),
                '{0}{1}: {2}'.format('  + ', key, to_str(new_value)),
            ])
        else:
            lines.append(
                '{0}{1}: {2}'.format(status, key, to_str(diff))
            )
    return '\n'.join(lines)


def generate_diff(path_1, path_2):
    file_1_data = json.load(open(path_1))
    file_2_data = json.load(open(path_2))

    diffs = {}

    added_keys = list(file_2_data.keys() - file_1_data.keys())
    removed_keys = list(file_1_data.keys() - file_2_data.keys())
    common_keys = list(file_1_data.keys() & file_2_data.keys())

    for key in added_keys:
        diffs[key] = {
            'status': '  + ',
            'diff': file_2_data.get(key),
        }

    for key in removed_keys:
        diffs[key] = {
            'status': '  - ',
            'diff': file_1_data.get(key),
        }

    for key in common_keys:
        value_1 = file_1_data.get(key)
        value_2 = file_2_data.get(key)
        if value_1 == value_2:
            diffs[key] = {
                'status': '    ',
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

    diffs = OrderedDict(sorted(diffs.items()))

    lines = ['{', stylish_formatter(diffs), '}']

    return '\n'.join(lines)
