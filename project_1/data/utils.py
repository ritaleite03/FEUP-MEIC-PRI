import json

def get_json(file_name):
    f = open(file_name)
    return json.load(f)

def write_to_file(file_name, file_content):
    with open(file_name, "w", encoding="UTF-8") as file:
        json.dump(file_content, file, ensure_ascii=False, indent=4)