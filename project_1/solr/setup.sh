#!/bin/bash

cd ../data

sudo docker run -p 8983:8983 --name pri_proj -v ${PWD}:/data -d solr:9

sudo docker exec pri_proj solr create_core -c diseases

curl -X POST -H 'Content-type:application/json' \
--data-binary "@../solr/schema.json" \
http://localhost:8983/solr/diseases/schema

sudo docker exec -it pri_proj bin/solr post -c diseases /data/data_complete.json