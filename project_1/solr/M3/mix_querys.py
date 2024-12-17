import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from query_embeddings import solr_knn_query, display_results, text_to_embedding
import requests


def solr_lexical_query(endpoint, collection, query):
    uri = f"{endpoint}/{collection}/select"
    data = {
        "query": f"{query}",
        "fields": "id Name score",
        "sort": "score desc",
        "params": {
            "defType": "edismax",
            "qf": "Name^2 Alias Overview^3 Can_Cause Specialty Caused_By Risk_Factors_List^4 Symptoms_List^4 Medical_Exams Transmission_Processes Anatomical_Location Treatments_List^4 Characteristics  Age_Onsets Opposit_Of Different_From Causes.Sections Symptoms.Sections Risk_factors.Sections Complications.Sections Prevention.Sections Diagnosis.Sections Treatment.Sections Genetic_Associations Symptoms.Text^3 Causes.Text^3 Risk_factors.Text^3 Complications.Text Prevention.Text Diagnosis.Text Treatment.Text^3",
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

    result_semantic = solr_knn_query(solr_endpoint, collection, embedding)
    result_semantic = result_semantic.get("response", {}).get("docs", [])
    top_score_semantic = result_semantic[0].get('score')
    lowest_score_semantic = result_semantic[-1].get('score')
    for result in result_semantic:
        result["score"] = (result.get('score') - lowest_score_semantic) / (top_score_semantic - lowest_score_semantic)

    for doc in result_semantic:
        print(f"* {doc.get('id')} {doc.get('Name')} [score: {doc.get('score'):.2f}]")
    
    result_lexical = solr_lexical_query(solr_endpoint, collection, query_text)
    result_lexical = result_lexical.get("response", {}).get("docs", [])
    top_score_lexical = result_lexical[0].get('score')
    lowest_score_lexical = result_lexical[-1].get('score')
    for result in result_lexical:
       result["score"] = (result.get('score') - lowest_score_lexical) / (top_score_lexical - lowest_score_lexical)
    
    print("\n")
    for doc in result_lexical:
        print(f"* {doc.get('id')} {doc.get('Name')} [score: {doc.get('score'):.2f}]")
    
    result_semantic_id = {item["id"]: item for item in result_semantic}
    result_lexical_id = {item["id"]: item for item in result_lexical}

    merge_result = []

    for key, value in result_semantic_id.items():
        if key in result_lexical_id.keys():
            print(value.get('score')*0.6  + result_lexical_id[key].get('score')*0.4 )
            merge_result.append({
                "id":key,
                "Name":value["Name"],
                "score":value.get('score')*0.6  + result_lexical_id[key].get('score')*0.4 
            })
            
        else:
            merge_result.append({
                "id": key,
                "Name":value["Name"],
                "score":value.get('score')*0.6 
            })
    
    for key, value in result_lexical_id.items():
       if key not in result_semantic_id.keys():
            merge_result.append({
                "id":key,
                "Name":value["Name"],
                "score":value.get('score')*0.4 
            })

    sorted = sorted(merge_result, key=lambda x: x.get('score'), reverse=True)

    for doc in sorted:
        print(f"* {doc.get('id')} {doc.get('Name')} [score: {doc.get('score'):.2f}]")



    





