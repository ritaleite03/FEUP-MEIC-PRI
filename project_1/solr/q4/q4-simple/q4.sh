python3 ../../query_solr.py --query query.json --collection diseases_simple
python3 ../../solr2trec.py > results_trec.txt
cat ../qrels.txt | python3 ../../qrels2trec.py > qrels_trec.txt
../../src/trec_eval/trec_eval qrels_trec.txt results_trec.txt
cat results_trec.txt | python3 ../../plot_pr.py --qrels qrels_trec.txt --output prec_rec.png
