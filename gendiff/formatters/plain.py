DIFF_STRINGS = {
    'added': "Property '{0}' was added with value: {1}",
    'removed': "Property '{0}' was removed",
    'changed': "Property '{0}' was updated. From {1} to {2}",
}


def to_str(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return value


def format_in_plain(diffs_dict, parent_path=''):
    lines = []
    for key, diffs in diffs_dict.items():
        property_path = f'{parent_path}.{key}' if parent_path else f'{key}'
        status = diffs.get('status')
        diff = diffs.get('diff')
        if status == 'added':
            lines.append(DIFF_STRINGS['added'].format(
                property_path, to_str(diff)
            ))
        elif status == 'removed':
            lines.append(DIFF_STRINGS['removed'].format(property_path))
        elif status == 'changed':
            old_value = diff.get('old_value')
            new_value = diff.get('new_value')
            lines.append(DIFF_STRINGS['changed'].format(
                property_path, to_str(old_value), to_str(new_value)
            ))
        elif status == 'nested':
            nested_value = format_in_plain(diff, property_path)
            lines.append(nested_value) if nested_value else nested_value
    return '\n'.join(lines)
