import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_json, save_json, sanitize_data

def clean(content):
    content_cleaned = {}

    for disease, information in content.items():
        if(disease == "Lists of diseases" or disease == "Disease" or disease == "List of phobias"):
            continue
        
        content_cleaned[disease] = information

        delete = []

        for k,v in information.items():
            if type(v) == dict:
                keys_del = []
                for k1,v1 in v.items():
                    if v1 == "":
                        keys_del.append(k1)
                for key in keys_del:
                    del v[key]

            if v == "":
                delete.append(k)
        
        for d in delete:
            del information[d]

        if "Specialty" in information:
            specialties = content_cleaned[disease]["Specialty"]
            specialties = [specialty[0].upper() + specialty[1:] for specialty in specialties if specialty != ""]

            final_specialties = []
            for specialty in specialties:
                if specialty in ["Infectious disease", "Pediatric", "Orthopedic", "Genetic"]:
                    final_specialties.append(specialty + "s")
                else:
                    final_specialties.append(specialty)

            content_cleaned[disease]["Specialty"] = final_specialties
    
    return content_cleaned


if __name__ == "__main__":
    wiki_new = load_json("raw_data/wikipedia_new.json")
    wiki_from_wikidata = load_json("raw_data/wikipedia_from_wikidata.json")

    wiki_new_cleaned = clean(sanitize_data(wiki_new))
    wiki_from_wikidata_cleaned = clean(sanitize_data(wiki_from_wikidata))

    save_json("data/wikipedia_new_clean.json", wiki_new_cleaned)
    save_json("data/wikipedia_from_wikidata_clean.json", wiki_from_wikidata_cleaned)