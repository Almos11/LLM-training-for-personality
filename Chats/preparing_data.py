import json
from datetime import datetime, timedelta
import os
import re

from deep_translator import GoogleTranslator

def translate_text(text):
    try:
        translation = GoogleTranslator(source='ru', target='en').translate(text)
    except:
        return ""
    
    if translation is None:
        return ""
    return translation

def process_json_files_in_folder(folder_path):
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        print(json_file)
        processed_data = process_messages(file_path)
        output_file_path = f"prepared_data/{json_file}"
        save_output(processed_data, output_file_path)

def remove_links(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.sub('', text)

def remove_code_blocks(text):
    code_pattern = re.compile(r'```.*?```', re.DOTALL)
    return code_pattern.sub('', text)

def process_messages(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        messages = json.load(file)
    messages = messages[::-1]
    all_messages_list = []
    index =  0
    cur_context = ""
    prev_date = None
    while index < len(messages):
        cur_output = ""
        cur_instruction = ""
        while index < len(messages):
            cur_date = datetime.fromisoformat(messages[index]['date'])
            if prev_date and cur_date - prev_date > timedelta(hours=12):
                cur_context = ""
                cur_instruction = ""
                prev_date = None
                break

            if messages[index]['out'] == False:
                cur_instruction += f'{messages[index]["message"]}\n'
                prev_date = cur_date
                index += 1
            else:
                break

        while index < len(messages):
            cur_date = datetime.fromisoformat(messages[index]['date'])
            if prev_date and cur_date - prev_date > timedelta(hours=12):
                cur_date = None
                break

            if messages[index]['out'] == True:
                cur_output += f'{messages[index]["message"]}\n'
                prev_date = cur_date
                index += 1
            else:
                break

        # cur_instruction = remove_links(cur_instruction)
        # cur_context = remove_links(cur_context)
        # cur_output = remove_links(cur_output)

        # cur_instruction = remove_code_blocks(cur_instruction)
        # cur_context = remove_code_blocks(cur_context)
        # cur_output = remove_code_blocks(cur_output)

        cur_instruction = translate_text(cur_instruction)
        cur_context = translate_text(cur_context)
        cur_output = translate_text(cur_output)

        if cur_instruction != "" and cur_output != "":
            all_messages_list.append({
                "instruction": cur_instruction,
                "input": cur_context,
                "output": cur_output

            })
        if cur_instruction != "":
            cur_context += f'\nU: {cur_instruction}\n'
        if cur_output != "":
            cur_context += f'\nR: {cur_output}\n'

        print(index, "/", len(messages), ". Count dialogs: ", len(all_messages_list))
    return all_messages_list

def save_output(output_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False)

process_json_files_in_folder("data")