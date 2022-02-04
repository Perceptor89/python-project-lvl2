from gendiff import generate_diff
import pytest


test_data = [
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
    'stylish',
    'tests/fixtures/plane_diff.txt'),
    ('tests/fixtures/file1.yaml', 'tests/fixtures/file2.yaml',
    'stylish',
    'tests/fixtures/plane_diff.txt'),
    ]


def get_correct_file(path):
    with open(path) as file:
        return file.read()


@pytest.mark.parametrize('file1, file2, format, correct_file_path', test_data)
def test_generate_diff(file1, file2, format, correct_file_path):
    correct_file = get_correct_file(correct_file_path)
    assert generate_diff(file1, file2) == correct_file
