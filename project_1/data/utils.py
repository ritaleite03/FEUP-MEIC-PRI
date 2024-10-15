import json
import re

def load_json(file_name):
    f = open(file_name)
    return json.load(f)

def save_json(file_name, file_content):
    with open(file_name, "w", encoding="UTF-8") as file:
        json.dump(file_content, file, ensure_ascii=False, indent=4)

def sanitize_data(data):
    def clean_json(data):
        if isinstance(data, dict):
            return {__clean_text(key): clean_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [clean_json(item) for item in data]
        elif isinstance(data, str):
            return __clean_text(data)
        else:
            return data
    
    cleaned_data = clean_json(data)

    return cleaned_data

def __clean_text(text):
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