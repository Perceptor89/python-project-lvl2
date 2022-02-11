from itertools import chain


REPLACER = '    '
STATUS_REPLACERS = {
    'added': '  + ',
    'removed': '  - ',
    'unchanged': '    ',
}
DIFF_STRING = '{0}{1}{2}: {3}'


def to_str(value, depth=0):
    output_dict = {
        bool: str(value).lower(),
        int: str(value),
        str: value,
        type(None): 'null',
    }

    if not isinstance(value, dict):
        if type(value) in output_dict.keys():
            return output_dict[type(value)]
        return str(value)

    lines = []
    depth_replacer = REPLACER * depth
    for key, _value in value.items():
        lines.append(DIFF_STRING.format(
            depth_replacer, REPLACER, key, to_str(_value, depth + 1)
        ))
    result = chain('{', lines, [depth_replacer + '}'])
    return '\n'.join(result)


def format_in_stylish(diffs_dict, depth=0):
    lines = []
    depth_replacer = REPLACER * depth
    for key, diff in diffs_dict.items():
        status = diff.get('status')
        diff = diff.get('diff')
        if status == 'nested':
            lines.append(DIFF_STRING.format(
                depth_replacer, REPLACER,
                key, format_in_stylish(diff, depth + 1)
            ))
        elif status == 'changed':
            old_value = diff.get('old_value')
            new_value = diff.get('new_value')
            lines.extend([
                DIFF_STRING.format(
                    depth_replacer, STATUS_REPLACERS['removed'],
                    key, to_str(old_value, depth + 1)
                ),
                DIFF_STRING.format(
                    depth_replacer, STATUS_REPLACERS['added'],
                    key, to_str(new_value, depth + 1)
                ),
            ])
        else:
            lines.append(DIFF_STRING.format(
                depth_replacer, STATUS_REPLACERS[status],
                key, to_str(diff, depth + 1)
            ))
    result = chain('{', lines, [depth_replacer + '}'])
    return '\n'.join(result)
