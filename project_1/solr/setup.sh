#!/bin/bash

docker stop pri_proj

docker rm pri_proj

docker run -p 8983:8983 --name pri_proj -v ${PWD}:/data -d solr:9
sleep 1

# COMPLEX CORE

docker exec pri_proj solr create_core -c diseases

curl http://localhost:8983/solr/diseases/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

docker cp ../solr/stopwords.txt pri_proj:/var/solr/data/diseases/conf

sleep 1

curl -X POST -H 'Content-type:application/json' \
    --data-binary "@schema.json" \
    http://localhost:8983/solr/diseases/schema

docker exec -it pri_proj bin/solr post -c diseases /data/solr_data.json

# SIMPLE CORE

docker exec pri_proj solr create_core -c diseases_simple

curl http://localhost:8983/solr/diseases_simple/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

curl -X POST -H 'Content-type:application/json' \
    --data-binary "@simple_schema.json" \
    http://localhost:8983/solr/diseases_simple/schema

docker exec -it pri_proj bin/solr post -c diseases_simple /data/solr_data.json

docker exec pri_proj solr create_core -c diseases_semantic

curl http://localhost:8983/solr/diseases_semantic/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

# SEMANTIC CORE

curl -X POST -H 'Content-type:application/json' \
    --data-binary "@semantic_schema.json" \
    http://localhost:8983/solr/diseases_semantic/schema

docker exec -it pri_proj bin/solr post -c diseases_semantic /data/semantic_data.json
