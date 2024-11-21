python3 ../../query_solr.py --query query_sys1.json
python3 ../../solr2trec.py > results_sys1_trec.txt
cat ../qrels.txt | python3  ../../qrels2trec.py > qrels_trec.txt
./../src/trec_eval/trec_eval qrels_trec.txt results_sys1_trec.txt
cat results_sys1_trec.txt | python3 ../../plot_pr.py --qrels qrels_trec.txt --output prec_rec_sys1_boosted.png
