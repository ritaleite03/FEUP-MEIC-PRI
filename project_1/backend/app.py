import os, sys
sys.path.append(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

from flask import Flask
from flask import request, abort
from flask_cors import CORS
import requests
import json
from solr.relevance_feedback import rocchio
from solr.query_embeddings import solr_knn_query, text_to_embedding

app = Flask(__name__)
CORS(app, resources={
        r"/search": {"origins": "*"}, 
        r"/relevance_feedback": {"origins": "*"}
    }
)

# query_solr = {
#     "fields": "id Name score vector",
#     "sort": "score desc",
#     "params": {
#         "defType": "edismax",
#         "qf": "Name^2 Alias Overview^3 Can_Cause Specialty Caused_By Risk_Factors_List^4 Symptoms_List^4 Medical_Exams Transmission_Processes Anatomical_Location Treatments_List^4 Characteristics  Age_Onsets Opposit_Of Different_From Causes.Sections Symptoms.Sections Risk_factors.Sections Complications.Sections Prevention.Sections Diagnosis.Sections Treatment.Sections Genetic_Associations Symptoms.Text^3 Causes.Text^3 Risk_factors.Text^3 Complications.Text Prevention.Text Diagnosis.Text Treatment.Text^3",
#         "start": 0,
#         "rows": 20,
#         "q.op": "OR",
#     },
# }


@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")

    solr_uri = "http://localhost:8983/solr"
    collection = "diseases_semantic"

    query_vector = text_to_embedding(query, convert_to_query_format=True)
    
    try:
        results = solr_knn_query(solr_uri, collection, query_vector)
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        abort(500)

    documents = solr_results_to_documents(results)
    return json.dumps(documents, indent=2, ensure_ascii=False)

@app.route("/relevance_feedback", methods=["POST"])
def relevance_feedback():
    query = request.json.get("query")
    relevant_vectors = request.json.get("relevant_vectors")
    non_relevant_vectors = request.json.get("non_relevant_vectors")

    query_vector = text_to_embedding(query, convert_to_query_format=False)
    query_vector = list(map(float, query_vector))

    new_query = rocchio(query_vector=query_vector, relevant_vectors=relevant_vectors, non_relevant_vectors=non_relevant_vectors)
    new_query = "[" + ",".join(map(str, new_query)) + "]"

    solr_uri = "http://localhost:8983/solr"
    collection = "diseases_semantic"

    try:
        results = solr_knn_query(solr_uri, collection, new_query)
    except Exception:
        abort(500)
    
    documents = solr_results_to_documents(results)

    return json.dumps(documents, indent=2, ensure_ascii=False)


def solr_results_to_documents(solr_results):
    file = open("../data/data.json")
    data = json.load(file)
    documents = []
    for doc in solr_results["response"]["docs"]:
        document = {"Name": doc["Name"], "id": doc["id"], "vector": doc["vector"]}
        document = {**document, **data[doc["Name"]]}
        documents.append(document)
    return documents


if __name__ == "__main__":
    app.run(host="localhost", port=5223, debug=True)
