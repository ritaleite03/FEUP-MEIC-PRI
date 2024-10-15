import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_json, save_json, sanitize_data

def clean(content):
    content_cleaned = {}

    for disease, information in content.items():
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
    file_content = load_json("wikipedia_diseases.json")

    content_cleaned = clean(sanitize_data(file_content))

    save_json("wikipedia.json", content_cleaned)