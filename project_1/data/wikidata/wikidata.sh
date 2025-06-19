#!/bin/bash

# set -e

ENDPOINT="https://query.wikidata.org/sparql"

FIRST_QUERY=$(< ./queries/first_query.rq)
SECOND_QUERY=$(< ./queries/second_query.rq)
THIRD_QUERY=$(< ./queries/third_query.rq)
FOURTH_QUERY=$(< ./queries/fourth_query.rq)


run_query () {
    while true
    do
        curl -f -G "${ENDPOINT}"                        \
            --data-urlencode "query=$1"                 \
            --data "format=json"                        \
            -o ./raw_data/$2
        
        if [[ "$?" -eq 0 ]]; then
            break
        else
            echo "WARNING: Query timed out during execution."
            echo "Running query again."
        fi
    done
}

run_query "${FIRST_QUERY}" "first_query.json"
run_query "${SECOND_QUERY}" "second_query.json"
run_query "${THIRD_QUERY}" "third_query.json"
run_query "${FOURTH_QUERY}" "fourth_query.json"

python3 clean.py
python3 merge.py