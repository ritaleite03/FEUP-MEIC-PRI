import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import *

KEYS = {
    'specialities': 'Specialty', 
    'symptoms': 'Symptoms List',
    'medicalExams': 'Medical Exams',
    'drugs': 'Drugs and Therapy',
    'transmissionProcesses': 'Transmission Processes',
    'anatomicalLocation': 'Anatomical Location',
    'characteristics': 'Characteristics',
    'diffFrom': 'Different From',
    'causes': 'Caused By',
    'canCause': 'Can Cause',
    'treatments': 'Treatments List',
    'geneticAssociations': 'Genetic Associations',
    'riskFactors': 'Risk Factors List',
    'ageOnsets': 'Age Onsets',
    'oppositOf': 'Opposit Of',
    'alias': 'Alias'
}

def clean(file_content):
    content_cleaned = {}
    file_content = file_content["results"]["bindings"]

    for disease in file_content:
        disease_name = disease["diseaseLabel"]["value"]
        temp = {}

        for k,v in KEYS.items():
            if k in disease and disease[k]["value"].strip() != "":
                items = disease[k]["value"].split(", ")
                if "unknown" in items:
                    items.remove("unknown")

                    if len(items) == 0:
                        continue

                final_items = []
                items_upper = [item.lower() for item in items if item.isupper()]
                items = map(lambda item: item.lower(), items)
                items = list(dict.fromkeys(items))

                for item in items:
                    if item in items_upper:
                        final_items.append(item.upper())
                    else:
                        final_items.append(item[0].upper() + item[1:])

                if k == "specialities":
                    final_specialties = []
                    print("before", final_items)
                    for specialty in final_items:
                        if specialty in ["Infectious disease", "Pediatric", "Orthopedic", "Genetic"]:
                            final_specialties.append(specialty + "s")
                        else:
                            final_specialties.append(specialty)

                    final_items = final_specialties
                
                temp[v] = final_items

        content_cleaned[disease_name] = temp

    return content_cleaned


if __name__ == "__main__":
    f1_content = get_json("./raw_data/first_query.json")
    f2_content = get_json("./raw_data/second_query.json")
    f3_content = get_json("./raw_data/third_query.json")
    f4_content = get_json("./raw_data/fourth_query.json")

    f1_cleaned = clean(f1_content)
    f2_cleaned = clean(f2_content)
    f3_cleaned = clean(f3_content)
    f4_cleaned = clean(f4_content)

    write_to_file("./data/first_query.json", f1_cleaned)
    write_to_file("./data/second_query.json", f2_cleaned)
    write_to_file("./data/third_query.json", f3_cleaned)
    write_to_file("./data/fourth_query.json", f4_cleaned)




