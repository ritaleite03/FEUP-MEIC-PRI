./../../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys3_trec.txt
cat all_results_sys3_trec.txt | python3 ../../plot_pr.py --qrels all_qrels_trec.txt --output prec_rec_sys2_simple.png