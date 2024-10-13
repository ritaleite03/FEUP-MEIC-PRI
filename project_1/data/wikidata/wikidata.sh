#!/bin/bash

set -e

ENDPOINT="https://query.wikidata.org/sparql"

FIRST_QUERY=$(< ./queries/first_query.rq)
SECOND_QUERY=$(< ./queries/second_query.rq)
THIRD_QUERY=$(< ./queries/third_query.rq)
FOURTH_QUERY=$(< ./queries/fourth_query.rq)

curl -f -G "${ENDPOINT}"                        \
    --data-urlencode "query=${FIRST_QUERY}"     \
    --data "format=json"                        \
    -o ./raw_data/first_query.json

curl -f -G "${ENDPOINT}"                        \
    --data-urlencode "query=${SECOND_QUERY}"    \
    --data "format=json"                        \
    -o ./raw_data/second_query.json

curl -f -G "${ENDPOINT}"                        \
    --data-urlencode "query=${THIRD_QUERY}"     \
    --data "format=json"                        \
    -o ./raw_data/third_query.json

curl -f -G "${ENDPOINT}"                        \
    --data-urlencode "query=${FOURTH_QUERY}"    \
    --data "format=json"                        \
    -o ./raw_data/fourth_query.json


python3 clean.py
python3 merge.py