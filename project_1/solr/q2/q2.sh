# Query simple schema
python3 ../query_solr.py --query query_sys1.json --collection diseases_simple > resultados_simple.json
python3 ../solr2trec.py --run-id diseases_simple < resultados_simple.json > results_sys1_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec1.txt
./../src/trec_eval/trec_eval qrels_trec1.txt results_sys1_trec.txt

# Query enhanced schema
python3 ../query_solr.py --query query_sys1.json > resultados_boosted.json
python3 ../solr2trec.py --run-id diseases_complex < resultados_boosted.json > results_sys2_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec2.txt
./../src/trec_eval/trec_eval qrels_trec2.txt results_sys2_trec.txt

# Query enhanced schema with weights
python3 ../query_solr.py --query query_sys3.json > resultados_weights.json
python3 ../solr2trec.py --run-id diseases_complex_weights < resultados_weights.json > results_sys3_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec3.txt
./../src/trec_eval/trec_eval qrels_trec3.txt results_sys3_trec.txt

# Figure simple schema
cat results_sys1_trec.txt | python3 ../plot_pr.py --qrels qrels_trec1.txt --output prec_rec_sys1_simple.png
# Figure enhanced schema
cat results_sys2_trec.txt | python3 ../plot_pr.py --qrels qrels_trec2.txt --output prec_rec_sys1_boosted.png
# Figure enhanced schema with weights
cat results_sys3_trec.txt | python3 ../plot_pr.py --qrels qrels_trec3.txt --output prec_rec_sys1_boosted_weights.png

# Figure all systems
python3 ../plot_pr_n.py \
  --qrels qrels_trec1.txt qrels_trec2.txt qrels_trec3.txt \
  --results results_sys1_trec.txt results_sys2_trec.txt results_sys3_trec.txt \
  --labels "Simple schema" "Enhanced schema" "Enhanced schema with customized weights" \
  --output prec_rec_sys1_all.png

rm resultados_simple.json resultados_boosted.json resultados_weights.json