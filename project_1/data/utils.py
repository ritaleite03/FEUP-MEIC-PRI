import json
import re

def load_json(file_name):
    f = open(file_name, "r", encoding="UTF-8")
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
    cleaned_text = re.sub(r'\[\d+\]', '', cleaned_text)
    cleaned_text = re.sub(r'\u2044', '/', cleaned_text)
    cleaned_text = re.sub(r'\u2014', '-', cleaned_text)
    cleaned_text = re.sub(r'\u2015', '-', cleaned_text)
    cleaned_text = cleaned_text.replace('–', '-')  
    cleaned_text = cleaned_text.replace('“', '\"')  
    cleaned_text = cleaned_text.replace('”', '\"') 
    cleaned_text = cleaned_text.replace('’', '\'') 
    cleaned_text = cleaned_text.replace('== References ==', '')
    return cleaned_text

def group_change_names(data):
    for key in data.keys():
        if "Caused by" in data[key]:
            data[key]["Causes List"] = data[key]["Caused by"]
            del data[key]["Caused by"]
        if "Drugs and Therapy" in data[key]:
            if "Treatments List" not in data[key]:
                data[key]["Treatments List"] = []
            data[key]["Treatments List"].extend(data[key]["Drugs and Therapy"])
            del data[key]["Drugs and Therapy"]
    return data

def delete_low_value_keys(data):
    for key in data:
        if "Age Onsets" in data[key]:
            del data[key]["Age Onsets"]
        if "Characteristics" in data[key]:
            del data[key]["Characteristics"]
        if "Opposit Of" in data[key]:
            del data[key]["Opposit Of"]
    return data
