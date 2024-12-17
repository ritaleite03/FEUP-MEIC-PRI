import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from query_embeddings import solr_knn_query, display_results, text_to_embedding
import requests


def solr_lexical_with_id_query(endpoint, collection, query, list_ids):
    id_filter = " ".join(list_ids)
    uri = f"{endpoint}/{collection}/select"
    data = {
        "query": f"{query}",
        "fields": "id Name score",
        "sort": "score desc",
        "params": {
            "defType": "edismax",
            "qf": "Name^2 Alias Overview^3 Can_Cause Specialty Caused_By Risk_Factors_List^4 Symptoms_List^4 Medical_Exams Transmission_Processes Anatomical_Location Treatments_List^4 Characteristics  Age_Onsets Opposit_Of Different_From Causes.Sections Symptoms.Sections Risk_factors.Sections Complications.Sections Prevention.Sections Diagnosis.Sections Treatment.Sections Genetic_Associations Symptoms.Text^3 Causes.Text^3 Risk_factors.Text^3 Complications.Text Prevention.Text Diagnosis.Text Treatment.Text^3",
            "fq": f"id:({id_filter})",
            "start": 0,
            "rows": 20,
            "q.op": "OR"
        }
    }

    try:
        # Send the POST request to Solr
        response = requests.post(uri, json=data)
        response.raise_for_status()  # Raise error if the request failed
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)
    
    return response.json()


if __name__ == "__main__":
    solr_endpoint = "http://localhost:8983/solr"
    collection = "diseases_semantic"

    query_text = input("Enter your query: ")
    embedding = text_to_embedding(query_text)

    resultSemantic = solr_knn_query(solr_endpoint, collection, embedding)
    display_results(resultSemantic)
    resultSemantic = resultSemantic.get("response", {}).get("docs", [])

    

    list_id = [item.get('id') for item in resultSemantic]

    print("\n")
    
    resultLexical = solr_lexical_with_id_query(solr_endpoint, collection, query_text, list_id)
    
    display_results(resultLexical)



    





