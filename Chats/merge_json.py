import json
import os

def merge(folder_path):
    combined_data = []
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
    for file_name in json_files:
        print(file_name)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
            combined_data.extend(data)
            print(len(data))

    with open('merged_data/combined.json', 'w') as outfile:
        json.dump(combined_data, outfile)
    
def custom_merge():
    combined_data = []
    file_path = "prepared_data/510058559.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
        combined_data.extend(data)

    with open('merged_data/one_dialog_510058559.json', 'w') as outfile:
        json.dump(combined_data, outfile)

# custom_merge()

merge("prepared_data")

def count_sample():
    with open('merged_data/combined.json', 'r', encoding='utf-8') as file:
        messages = json.load(file)
    print(len(messages))

count_sample()