import json

if __name__ == "__main__":
    with open("../data/data.json", "r", encoding="UTF-8") as file:
        content = json.load(file)

    solr_documents = []

    for key, value in content.items():
        new_entry = {}
        new_entry["id"] = "_" + key.lower().replace(" ", "_")
        new_entry["Name"] = key
        for k, v in value.items():
            if not isinstance(v, dict):
                new_entry[k.replace(" ", "_")] = v
                continue
            sections = []
            text = []
            for s, t in v.items():
                if s != "Summary":
                    sections.append(s)
                text.append(t)
            entry = {"Text": text}
            if sections:
                entry["Sections"] = sections
            new_entry[k.replace(" ", "_")] = entry
        solr_documents.append(new_entry)

    with open("./solr_data.json", "w", encoding="UTF-8") as file:
        json.dump(solr_documents, file, indent=4, ensure_ascii=False)
