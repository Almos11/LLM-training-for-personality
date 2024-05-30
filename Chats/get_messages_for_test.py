import json
import random

random.seed(42)

def get_messages_without_context(file_path, output_file_name, max_messages = 40):
    with open(file_path, 'r') as file:
        data = json.load(file)

    random.shuffle(data)
    test_messages = []
    answers = []
    for message in data:
        if len(test_messages) == max_messages:
            break
        if message['input'] == "" and message['instruction'][-1] == '?' and message['output'][-1] != '?':
            test_messages.append(message['instruction'])
            answers.append(message['output'])

    with open(f"{output_file_name}_question.json", 'w') as output_file:
        json.dump(test_messages, output_file, ensure_ascii=False, indent=4)

    with open(f"{output_file_name}_answer.json", 'w') as output_file:
        json.dump(answers, output_file, ensure_ascii=False, indent=4)


def get_messages_with_context(file_path, output_file_name, max_messages = 40):
    with open(file_path, 'r') as file:
        data = json.load(file)

    random.shuffle(data)
    test_messages = []
    answers = []
    for message in data:
        if len(test_messages) == max_messages:
            break
        if message['input'] != "" and len(message['input']) < 50 and message['instruction'][-1] == '?' and message['output'][-1] != '?':
            test_messages.append({
                'question': message['instruction'],
                'context': message['input']
                })
            answers.append(message['output'])

    with open(f"{output_file_name}_question.json", 'w') as output_file:
        json.dump(test_messages, output_file, ensure_ascii=False, indent=4)

    with open(f"{output_file_name}_answer.json", 'w') as output_file:
        json.dump(answers, output_file, ensure_ascii=False, indent=4)

get_messages_without_context("merged_data/combined.json", "test_data/without_context")

get_messages_with_context("merged_data/combined.json", "test_data/with_context")