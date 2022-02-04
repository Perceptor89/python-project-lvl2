import json
import yaml


def parse_file(file_path):
    extension = file_path.split('.')[-1]
    if extension in ('yaml', 'yml'):
        with open(file_path) as file:
            return yaml.safe_load(file)
    if extension == 'json':
        with open(file_path) as file:
            return json.load(file)
