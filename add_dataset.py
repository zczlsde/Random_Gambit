import os
import json

def read_txt_files_in_folder(folder_path):
    txt_files_data = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".efg"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                file_content = file.read()
                txt_files_data.append({"text": file_content})
    
    print(txt_files_data)
    return txt_files_data

def append_to_json_file(json_file_path, data):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    if not isinstance(existing_data, list):
        raise ValueError("The JSON file does not contain a list.")
    
    existing_data.extend(data)
    
    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

folder_path = 'imperfect_info_game/'
json_file_path = 'pretrain_data.json'

txt_files_data = read_txt_files_in_folder(folder_path)
append_to_json_file(json_file_path, txt_files_data)
