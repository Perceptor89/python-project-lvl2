from collections import OrderedDict
from gendiff.parser import parse_file
from itertools import chain


REPLACER = '    '


def to_str(value, depth=0):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        lines = []
        depth_replacer = REPLACER * depth
        for k, v in value.items():
            if isinstance(v, dict):
                lines.append('{0}{1}{2}: {3}'.format(
                    depth_replacer, REPLACER, k, to_str(v, depth + 1)
                ))
            else:
                lines.append('{0}{1}{2}: {3}'.format(
                    depth_replacer, REPLACER, k, to_str(v)
                ))
        result = chain('{', lines, [depth_replacer + '}'])
        return '\n'.join(result)
    else:
        return str(value)


def stylish_formatter(diffs_dict, depth=0):
    lines = []
    depth_replacer = REPLACER * depth
    for key, diff in diffs_dict.items():
        status = diff.get('status')
        diff = diff.get('diff')
        if status == 'nested':
            lines.append('{0}{1}{2}: {3}'.format(
                depth_replacer, REPLACER, key, stylish_formatter(
                    diff, depth + 1
                )
            ))
        elif status == 'changed':
            old_value = diff.get('old_value')
            new_value = diff.get('new_value')
            lines.extend([
                '{0}{1}{2}: {3}'.format(
                    depth_replacer, '  - ', key, to_str(old_value, depth + 1)
                ),
                '{0}{1}{2}: {3}'.format(
                    depth_replacer, '  + ', key, to_str(new_value, depth + 1)
                ),
            ])
        else:
            lines.append('{0}{1}{2}: {3}'.format(
                depth_replacer, status, key, to_str(diff, depth + 1)
            ))
    result = chain('{', lines, [depth_replacer + '}'])
    return '\n'.join(result)


def get_diffs_dict(file_1_data, file_2_data):
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
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            diffs[key] = {
                'status': 'nested',
                'diff': get_diffs_dict(value_1, value_2),
            }
        elif value_1 == value_2:
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

    return OrderedDict(sorted(diffs.items()))


def generate_diff(path_1, path_2):
    file_1_data = parse_file(path_1)
    file_2_data = parse_file(path_2)

    diffs_dict = get_diffs_dict(file_1_data, file_2_data)
    diffs_in_stylish = stylish_formatter(diffs_dict)

    return diffs_in_stylish
