import json


def generate_diff(path_1, path_2):
    file_1_data = json.load(open(path_1))
    file_2_data = json.load(open(path_2))

    file_1_keys = file_1_data.keys()
    file_2_keys = file_2_data.keys()

    file_1_only_keys = file_1_keys - file_2_keys
    file_2_only_keys = file_2_keys - file_1_keys
    common_keys = file_1_keys & file_2_keys
    all_unique_keys = file_1_keys | file_2_keys

    diff_string = ''
    for key in sorted(all_unique_keys):
        if key in file_1_only_keys:
            diff_string += f' - {key}: {file_1_data[key]}\n'
        elif key in file_2_only_keys:
            diff_string += f' + {key}: {file_2_data[key]}\n'
        elif key in common_keys:
            if file_1_data[key] == file_2_data[key]:
                diff_string += f'   {key}: {file_1_data[key]}\n'
            else:
                diff_string += f' - {key}: {file_1_data[key]}\n'
                diff_string += f' + {key}: {file_2_data[key]}\n'
    
    return '{\n' + diff_string + '}'




    
