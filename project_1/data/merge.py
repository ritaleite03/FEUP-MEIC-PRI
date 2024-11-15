from utils import load_json, save_json, delete_low_value_keys

def merge(wikidata_content, wikipedia_content):
    wikipedia_diseases = {disease.lower(): disease for disease in wikipedia_content.keys()}

    for wikidata_disease, wikidata_information in wikidata_content.items():
        if wikidata_disease.lower() in wikipedia_diseases:
            disease = wikipedia_diseases[wikidata_disease.lower()]
            merge_data(wikidata_information, wikipedia_content[disease])

    return wikipedia_content
    

def merge_data(wikidata_disease_information, wikipedia_disease_information):
    for k,v in wikidata_disease_information.items():
        wikipedia_disease_information.update({k: v})


if __name__ == "__main__":
    wikidata_content = load_json("./wikidata/wikidata.json")
    wikipedia_content = load_json("./wikipedia/wikipedia.json")

    content = merge(wikidata_content, wikipedia_content)

    content = delete_low_value_keys(content)

    solr_documents = []

    for key, value in content.items():
        new_entry = {}
        new_entry["id"] = "_" + key.lower().replace(" ", "_")
        new_entry["Name"] = key
        for k, v in value.items():
            new_entry[k.replace(" ", "_")] = v
        solr_documents.append(new_entry)

    save_json('data.json', solr_documents)