from utils import *

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
    wikidata_content = get_json("./wikidata/wikidata.json")
    wikipedia_content = get_json("./wikipedia/wikipedia_diseases.json")

    content = merge(wikidata_content, wikipedia_content)

    write_to_file("data.json", content)

