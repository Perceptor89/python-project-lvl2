import pytest
import json
from gendiff import generate_diff


TESTS_DATA = [
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
     'stylish', 'tests/fixtures/plane_diff.txt'),
    ('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml',
     'stylish', 'tests/fixtures/plane_diff.txt'),
    ('tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json',
     'stylish', 'tests/fixtures/nested_diff.txt'),
    ('tests/fixtures/file1_nested.yaml', 'tests/fixtures/file2_nested.yaml',
     'stylish', 'tests/fixtures/nested_diff.txt'),
    ('tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json',
     'plain', 'tests/fixtures/nested_diff_in_plain.txt'),
    ('tests/fixtures/file1_nested.yaml', 'tests/fixtures/file2_nested.yaml',
     'plain', 'tests/fixtures/nested_diff_in_plain.txt'),
    ('tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json',
     'json', 'tests/fixtures/nested_diff_in_json.txt'),
    ('tests/fixtures/file1_nested.yaml', 'tests/fixtures/file2_nested.yaml',
     'json', 'tests/fixtures/nested_diff_in_json.txt'),
]


def get_correct_file(path, fmt):
    with open(path) as file:
        if fmt == 'json':
            return json.loads(file.read())
        else:
            return file.read()


@pytest.mark.parametrize('file1, file2, fmt, correct_path', TESTS_DATA)
def test_generate_diff(file1, file2, fmt, correct_path):
    correct_file = get_correct_file(correct_path, fmt)
    if fmt == 'json':
        assert json.loads(generate_diff(file1, file2, fmt)) == correct_file
    else:
        assert generate_diff(file1, file2, fmt) == correct_file
