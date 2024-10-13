import re
import json

def clean_text(text):
    cleaned_text = re.sub(r"(?<!\d):[\u200a-\u200f]\d+", ' ', text)
    cleaned_text = re.sub(r'[\u200a-\u200f]', '', cleaned_text)
    cleaned_text = re.sub(r"(?<!\d):\d+", ' ', cleaned_text)
    cleaned_text = ''.join(c for c in cleaned_text if c.isprintable())
    cleaned_text = re.sub(r'[\n\t\s]+', ' ', cleaned_text)
    cleaned_text = re.sub(r'\u2044', '/', cleaned_text)
    cleaned_text = cleaned_text.replace('–', '-')  
    cleaned_text = cleaned_text.replace('“', '\"')  
    cleaned_text = cleaned_text.replace('”', '\"') 
    cleaned_text = cleaned_text.replace('’', '\'') 
    cleaned_text = cleaned_text.replace('== References ==', '')
    return cleaned_text

def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    def clean_json(data):
        if isinstance(data, dict):
            return {clean_text(key): clean_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_json(item) for item in data]
        elif isinstance(data, str):
            return clean_text(data)
        else:
            return data

    cleaned_data = clean_json(data)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


input_filename = 'data.json'
output_filename = 'data_clean.json'
process_json_file(input_filename, output_filename)