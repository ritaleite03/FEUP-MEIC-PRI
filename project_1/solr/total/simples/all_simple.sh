./../../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys1_trec.txt
cat all_results_sys1_trec.txt | python3 ../../plot_pr.py --qrels all_qrels_trec.txt --output prec_rec_sys1_simple.png