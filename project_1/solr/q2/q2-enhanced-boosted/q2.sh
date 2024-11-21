python3 ../../query_solr.py --query query_sys3.json --collection diseases
python3 ../solr2trec.py > results_trec.txt
cat ../qrels.txt | python3 ../qrels2trec.py > qrels_trec.txt
../../src/trec_eval/trec_eval -q qrels_trec.txt results_trec.txt
cat results_trec.txt | python3 ../../plot_pr.py --qrels qrels_trec.txt --output prec_rec.png