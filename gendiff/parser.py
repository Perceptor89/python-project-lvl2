import json
import yaml


def parse(data, format):
    if format in ('yaml', 'yml'):
        return yaml.safe_load(data)
    if format == 'json':
        return json.load(data)
