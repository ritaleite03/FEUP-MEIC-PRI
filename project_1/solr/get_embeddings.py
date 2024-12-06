import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

def merge_subsections_into_text(section):
    if section == "":
        return ""
    
    combined_text = ""
    for sub_section in section:
        section_text = section.get(sub_section)
        section_text = " ".join(section_text)
        combined_text += section_text + " "
    
    return combined_text

if __name__ == "__main__":
    f = open("solr_data.json", "r", encoding="UTF-8")
    data = json.load(f)

    SECTIONS_TO_IGNORE = ['id', 'Total_Revisions', 'Last_Revision_Date'] 
    
    length = len(data)
    current = 1

    for document in data:
        print(str(current) + "/" + str(length))
        combined_text = ""

        for section, info in document.items():

            if section in SECTIONS_TO_IGNORE:
                continue
            
            section_text = ""
            if type(info) == str:
                section_text = info
            elif type(info) == list:
                section_text = " ".join(info)
            elif type(info) == dict:
                section_text = merge_subsections_into_text(info)
            else:
                print("UNEXPECTED TYPE: " + type(info))
            
            combined_text += section_text + " "

        document["vector"] = get_embedding(combined_text)
        current += 1

    with open("semantic_data.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
