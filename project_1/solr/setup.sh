#!/bin/bash

cd ../data

docker stop pri_proj

docker rm pri_proj

docker run -p 8983:8983 --name pri_proj -v ${PWD}:/data -d solr:9
sleep 1

docker exec pri_proj solr create_core -c diseases

curl http://localhost:8983/solr/diseases/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

curl -X POST -H 'Content-type:application/json' \
  --data-binary "@../solr/schema.json" \
  http://localhost:8983/solr/diseases/schema

docker exec -it pri_proj bin/solr post -c diseases /data/data_complete.json

