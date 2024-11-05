import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils import load_json, save_json, sanitize_data


def compare_json(json1, json2):
    i, j, k = 0, 0, 0
    if isinstance(json1, dict) and isinstance(json2, dict):

        keys1 = {key.lower() for key in json1.keys()}
        print(f"Diseases in wikipedia_new_clean: {len(keys1)}")
        keys2 = {key.lower() for key in json2.keys()}
        print(f"Diseases in wikipedia_from_wikidata: {len(keys2)}")
        

        for key in keys1:
            if key not in keys2:
                i += 1
                #print(f"Key '{key}' found in the first JSON but not in the second.")
            else:
                j += 1
                #print(f"Key '{key}' found in both.")

        for key in keys2:
            if key not in keys1:
                k += 1
                #print(f"Key '{key}' found in the second JSON but not in the first.")

    print(f"only in first JSON: {i}")
    print(f"only in second JSON: {k}")
    print(f"found in both: {j}")
    

def merge_json(json1, json2):
    merged_data = json1.copy()  

    for key, value in json2.items():
        if key.lower() not in (k.lower() for k in merged_data.keys()):
            merged_data[key] = value

    return merged_data

file1 = '../../wikipedia/New/wikipedia_new_clean.json'
file2 = 'wikipedia_from_wikidata_clean.json'
merged_file = '../../wikidata/New/wikipedia_complete.json'

json_data1 = load_json(file1)
json_data2 = load_json(file2)

compare_json(json_data1, json_data2)

merged_data = merge_json(json_data1, json_data2)

save_json(merged_file, merged_data)

print(f"Merged JSON saved to {merged_file}")
