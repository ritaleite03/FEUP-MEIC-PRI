import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_json, save_json

def merge_json(json1, json2):
    merged_data = json1.copy()  

    for key, value in json2.items():
        if key.lower() not in (k.lower() for k in merged_data.keys()):
            merged_data[key] = value

    return merged_data

if __name__ == "__main__":
    wikipedia_new = load_json('data/wikipedia_new_clean.json')
    wikipedia_from_wikidata = load_json('data/wikipedia_from_wikidata_clean.json')

    merged_data = merge_json(wikipedia_new, wikipedia_from_wikidata)

    save_json('wikipedia.json', merged_data)