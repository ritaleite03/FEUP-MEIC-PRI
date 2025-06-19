all: clean wikidata wikipedia merge

clean:
	rm -f wikidata/data/*.json
	rm -f wikidata/raw_data/*.json
	rm -f wikidata/wikidata.json

	rm -f wikipedia/raw_data/*.json
	rm -f wikipedia/data/*.json
	rm -f wikipedia/wikipedia.json

	rm -f data.json

.PHONY: wikidata
wikidata:
	cd wikidata && ./wikidata.sh
	cd ..

.PHONY: wikipedia
wikipedia:
	cd wikipedia && ./wikipedia.sh
	cd ..

merge:
	python3 merge.py