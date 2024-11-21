#!/usr/bin/env python3

import argparse
import json
import sys


def solr_to_trec(solr_response, run_id="run0"):
    """
    Converts Solr search results to TREC format and writes the results to STDOUT.

    Format:
    qid     iter    docno       rank    sim     run_id
    0       Q0      M.EIC028    1       0.80    run0

    Arguments:
    - solr_response: Dictionary containing Solr response with document IDs and scores.
    - run_id: Identifier for the experiment or system (default: run0).

    Output:
    - Writes the converted results to STDOUT.
    """
    try:
        # Extract the document results from the Solr response
        docs = solr_response["response"]["docs"]

        # Enumerate through the results and write them in TREC format
        for rank, doc in enumerate(docs, start=1):
            print(f"2 Q0 {doc['id']} {rank} {doc['score']} {run_id}")

    except KeyError:
        print("Error: Invalid Solr response format. 'docs' key not found.")
        sys.exit(1)


if __name__ == "__main__":
    # Set up argument parsing for command-line interface
    parser = argparse.ArgumentParser(description="Convert Solr results to TREC format.")
    # Add argument for optional run ID
    parser.add_argument(
        "--run-id",
        type=str,
        default="run0",
        help="Experiment or system identifier (default: run0).",
    )   
    # Parse command-line arguments
    args = parser.parse_args()
    # Load Solr response from STDIN
    input_file = 'resultados.json'

    # Lendo o conteúdo do ficheiro
    with open(input_file, 'r', encoding='utf-8') as f:
        solr_response = json.load(f)

    solr_to_trec(solr_response, args.run_id)
