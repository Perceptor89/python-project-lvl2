import pytest
import json
from gendiff import generate_diff


def get_test_data():
    with open('tests/fixtures/test_data.txt', 'r') as file:
        data = file.read().splitlines()

    test_data = []
    index = 0
    while index < len(data):
        current_test_data = tuple(data[index:index + 4])
        test_data.append(current_test_data)
        index += 4

    return test_data


def get_correct_file(path, fmt):
    with open(path) as file:
        if fmt == 'json':
            return json.loads(file.read())
        else:
            return file.read()


@pytest.mark.parametrize('file1, file2, fmt, correct_path', get_test_data())
def test_generate_diff(file1, file2, fmt, correct_path):
    correct_file = get_correct_file(correct_path, fmt)
    if fmt == 'json':
        assert json.loads(generate_diff(file1, file2, fmt)) == correct_file
    else:
        assert generate_diff(file1, file2, fmt) == correct_file
