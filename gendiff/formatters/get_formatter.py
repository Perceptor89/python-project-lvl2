from gendiff.formatters.stylish import format_in_stylish
from gendiff.formatters.plain import format_in_plain
from gendiff.formatters.json import format_in_json


def get_formatter(format_name: str):
    formatters = {
        'stylish': format_in_stylish,
        'plain': format_in_plain,
        'json': format_in_json,
    }
    return formatters.get(format_name)
