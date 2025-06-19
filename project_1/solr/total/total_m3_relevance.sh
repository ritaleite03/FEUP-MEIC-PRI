sed 's/^./1/' ../q1/results_sys1_relevance_trec.txt > temp_q1.txt
sed 's/^./2/' ../q2/results_sys1_relevance_trec.txt > temp_q2.txt
sed 's/^./3/' ../q3/results_sys1_relevance_trec.txt > temp_q3.txt
sed 's/^./4/' ../q4/results_sys1_relevance_trec.txt > temp_q4.txt
cat temp_q4.txt temp_q3.txt temp_q2.txt temp_q1.txt > all_results_sys1_trec.txt

sed 's/^./1/' ../q1/results_sys2_relevance_trec.txt > temp_q1.txt
sed 's/^./2/' ../q2/results_sys2_relevance_trec.txt > temp_q2.txt
sed 's/^./3/' ../q3/results_sys2_relevance_trec.txt > temp_q3.txt
sed 's/^./4/' ../q4/results_sys2_relevance_trec.txt > temp_q4.txt
cat temp_q4.txt temp_q3.txt temp_q2.txt temp_q1.txt > all_results_sys2_trec.txt

sed 's/^./1/' ../q1/results_sys3_relevance_trec.txt > temp_q1.txt
sed 's/^./2/' ../q2/results_sys3_relevance_trec.txt > temp_q2.txt
sed 's/^./3/' ../q3/results_sys3_relevance_trec.txt > temp_q3.txt
sed 's/^./4/' ../q4/results_sys3_relevance_trec.txt > temp_q4.txt
cat temp_q4.txt temp_q3.txt temp_q2.txt temp_q1.txt > all_results_sys3_trec.txt

sed 's/^./1/' ../q1/results_sys4_relevance_trec.txt > temp_q1.txt
sed 's/^./2/' ../q2/results_sys4_relevance_trec.txt > temp_q2.txt
sed 's/^./3/' ../q3/results_sys4_relevance_trec.txt > temp_q3.txt
sed 's/^./4/' ../q4/results_sys4_relevance_trec.txt > temp_q4.txt
cat temp_q4.txt temp_q3.txt temp_q2.txt temp_q1.txt > all_results_sys4_trec.txt

sed 's/^./1/' ../q1/qrels_trec.txt > temp_q1.txt
sed 's/^./2/' ../q2/qrels_trec.txt > temp_q2.txt
sed 's/^./3/' ../q3/qrels_trec.txt > temp_q3.txt
sed 's/^./4/' ../q4/qrels_trec.txt > temp_q4.txt
cat temp_q4.txt temp_q3.txt temp_q2.txt temp_q1.txt > all_qrels_trec.txt

rm temp_q1.txt temp_q2.txt temp_q3.txt temp_q4.txt

./../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys1_trec.txt
# cat all_results_sys1_trec.txt | python3 ../plot_pr.py --qrels all_qrels_trec1.txt --output prec_rec_sys1_relevance.png

./../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys2_trec.txt
# cat all_results_sys2_trec.txt | python3 ../plot_pr.py --qrels all_qrels_trec3.txt --output prec_rec_sys2_relevance.png

./../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys3_trec.txt
# cat all_results_sys3_trec.txt | python3 ../plot_pr.py --qrels all_qrels_trec2.txt --output prec_rec_sys3_relevance.png

./../src/trec_eval/trec_eval all_qrels_trec.txt all_results_sys4_trec.txt
# cat all_results_sys4_trec.txt | python3 ../plot_pr.py --qrels all_qrels_trec1.txt --output prec_rec_sys4_relevance.png

# Figure all systems
# python3 ../plot_pr_n.py \
#   --qrels all_qrels_trec1.txt all_qrels_trec2.txt all_qrels_trec2.txt \
#   --results all_results_sys1_trec.txt all_results_sys2_trec.txt all_results_sys3_trec.txt \
#   --labels "System 1" "System 2" "System 3" \
#   --output prec_rec_sys1_all.png

python3 ../plot_pr_n.py \
  --qrels all_qrels_trec.txt all_qrels_trec.txt all_qrels_trec.txt all_qrels_trec.txt\
  --results all_results_sys1_trec.txt all_results_sys2_trec.txt all_results_sys3_trec.txt all_results_sys4_trec.txt\
  --labels "System 1" "System 2" "System 3" "System 4"\
  --output prec_rec_sys_all_all_relevance.png

rm all_results_sys1_trec.txt all_results_sys2_trec.txt all_results_sys3_trec.txt all_results_sys4_trec.txt
rm all_qrels_trec.txt
