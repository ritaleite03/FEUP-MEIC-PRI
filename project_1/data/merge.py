from utils import delete_low_value_keys, load_json, save_json, group_change_names, delete_low_value_keys
import json

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4) 


def merge(wikidata_content, wikipedia_content):
    wikipedia_diseases = {disease.lower(): disease for disease in wikipedia_content.keys()}

    for wikidata_disease, wikidata_information in wikidata_content.items():
        if wikidata_disease.lower() in wikipedia_diseases:
            disease = wikipedia_diseases[wikidata_disease.lower()]
            merge_data(wikidata_information, wikipedia_content[disease])

    return wikipedia_content

def merge_data(wikidata_disease_information, wikipedia_disease_information):
    for k, v in wikidata_disease_information.items():
        wikipedia_disease_information[k] = v

if __name__ == "__main__":

    wikidata_content = load_json("./wikidata/wikidata.json")
    wikipedia_content = load_json("./wikipedia/wikipedia.json")

    content = merge(wikidata_content, wikipedia_content)

    content = group_change_names(content)

    content = delete_low_value_keys(content)

    solr_documents = []

    for key, value in content.items():
        new_entry = {}
        new_entry["id"] = key  
        for k, v in value.items():
            new_entry[k] = v
        solr_documents.append(new_entry)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(solr_documents, f, ensure_ascii=False, indent=4)
