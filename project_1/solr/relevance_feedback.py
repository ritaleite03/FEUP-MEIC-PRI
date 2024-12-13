import requests
import sys
import json

def relevance_feedback(solr_uri, collection, relevant_documents):
    URL = f"{solr_uri}/{collection}/select"
    HEADERS = { "Content-Type": "application/x-www-form-urlencoded" }

    RELEVANT_DOCUMENTS = {}

    for relevant_document in relevant_documents:
        DATA = {
            "q": f"{{!mlt f=vector mintf=1 mindf=1}}{relevant_document}",
            "fl": "id,Name,score",
            "wt": "json"
        }

        try:
            response = requests.post(url=URL, data=DATA, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error querying Solr: {e}")
            sys.exit(1)

        results = response.json()
        new_documents = results['response']['docs']

        for new_document in new_documents:
            id = new_document['Name']
            score = new_document['score']

            if id in RELEVANT_DOCUMENTS:
                RELEVANT_DOCUMENTS[id] =  RELEVANT_DOCUMENTS[id] + score
            else:
                RELEVANT_DOCUMENTS[id] = score

    sorted_documents = {k:v for k,v in sorted(RELEVANT_DOCUMENTS.items(), key=lambda item: item[1], reverse=True)}

    top_20 = {}

    for i,(k,v) in enumerate(sorted_documents.items()):
        if i == 20:
            break
        
        top_20[k] = v

    with open("relevance_results.json", "w", encoding="UTF-8") as file:
        json.dump(top_20, file, indent=4, ensure_ascii=False)

def main():
    solr_uri = "http://localhost:8983/solr"
    collection = "diseases_semantic"
    relevant_documents = [
        "_pneumatosis",
        "_black_lung_disease",
        "_hypersensitivity_pneumonitis",
        "_occupational_lung_disease",
        "_asbestosis",
        "_emphysema",
        "_chronic_obstructive_pulmonary_disease",
        "_respiratory_disease",
        "_pneumoconiosis",
        "_berylliosis",
        "_chemical_pneumonitis",
        "_bird_fancier's_lung",
        "_bagassosis",
        "_lung_cancer",
        "_occupational_asthma"
    ]

    relevance_feedback(solr_uri=solr_uri, collection=collection, relevant_documents=relevant_documents)

if __name__ == "__main__":
    main()