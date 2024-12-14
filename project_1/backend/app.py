from flask import Flask
from flask import request
import sys
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/search": {"origins": "*"}})

query_solr = {
    "fields": "id Name score",
    "sort": "score desc",
    "params": {
        "defType": "edismax",
        "qf": "Name^2 Alias Overview^3 Can_Cause Specialty Caused_By Risk_Factors_List^4 Symptoms_List^4 Medical_Exams Transmission_Processes Anatomical_Location Treatments_List^4 Characteristics  Age_Onsets Opposit_Of Different_From Causes.Sections Symptoms.Sections Risk_factors.Sections Complications.Sections Prevention.Sections Diagnosis.Sections Treatment.Sections Genetic_Associations Symptoms.Text^3 Causes.Text^3 Risk_factors.Text^3 Complications.Text Prevention.Text Diagnosis.Text Treatment.Text^3",
        "start": 0,
        "rows": 20,
        "q.op": "OR",
    },
}


@app.route("/search", methods=["POST"])  # Alterar para POST
def search():
    user_query = request.json.get("query")  # Alterado para obter o JSON do corpo
    query_solr["query"] = user_query
    print(user_query)
    solr_uri = "http://localhost:8983/solr"
    collection = "diseases_semantic"

    uri = f"{solr_uri}/{collection}/select"

    try:
        response = requests.post(uri, json=query_solr)
        response.raise_for_status()  # Levanta erro se a solicitação falhar
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    solr_results = response.json()

    documents = solr_results_to_documents(solr_results)
    print(documents)
    return json.dumps(documents, indent=2, ensure_ascii=False)


def solr_results_to_documents(solr_results):
    file = open("../data/data.json")
    data = json.load(file)
    documents = []
    for doc in solr_results["response"]["docs"]:
        document = {"Name": doc["Name"], "id": doc["id"]}
        document = {**document, **data[doc["Name"]]}
        documents.append(document)
    return documents


if __name__ == "__main__":
    app.run(host="localhost", port=5223, debug=True)
