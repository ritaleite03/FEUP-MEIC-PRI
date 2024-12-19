### M2 ###

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

# # Figure simple schema
# cat results_sys1_trec.txt | python3 ../plot_pr.py --qrels qrels_trec1.txt --output prec_rec_sys1_simple.png
# # Figure enhanced schema
# cat results_sys2_trec.txt | python3 ../plot_pr.py --qrels qrels_trec2.txt --output prec_rec_sys1_boosted.png
# # Figure enhanced schema with weights
# cat results_sys3_trec.txt | python3 ../plot_pr.py --qrels qrels_trec3.txt --output prec_rec_sys1_boosted_weights.png

# Figure all systems
python3 ../plot_pr_n.py \
  --qrels qrels_trec1.txt qrels_trec2.txt qrels_trec3.txt \
  --results results_sys1_trec.txt results_sys2_trec.txt results_sys3_trec.txt \
  --labels "Simple schema" "Enhanced schema" "Enhanced schema with customized weights" \
  --output prec_rec_sys1_all.png

### M3 ###

# 1.0 semantic 0.0 lexical
python3 ../M3/mix_querys.py --query "persistent fatigue exhaustion" --semantic 1.0 --lexical 0.0 > resultados_simple.json
python3 ../solr2trec.py --run-id weight_0.5_0.5 < resultados_simple.json > results_sys0_semantic_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec0.txt
./../src/trec_eval/trec_eval qrels_trec0.txt results_sys0_semantic_trec.txt
# cat results_sys0_semantic_trec.txt | python3 ../plot_pr.py --qrels qrels_trec0.txt --output prec_rec_sys1_semantic.png

# 0.5 semantic 0.5 lexical
python3 ../M3/mix_querys.py --query "persistent fatigue exhaustion" --semantic 0.5 --lexical 0.5 > resultados_simple.json
python3 ../solr2trec.py --run-id weight_0.5_0.5 < resultados_simple.json > results_sys1_semantic_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec1.txt
./../src/trec_eval/trec_eval qrels_trec1.txt results_sys1_semantic_trec.txt
# cat results_sys1_semantic_trec.txt | python3 ../plot_pr.py --qrels qrels_trec1.txt --output prec_rec_sys1_semantic.png

# 0.7 semantic 0.3 lexical
python3 ../M3/mix_querys.py --query "persistent fatigue exhaustion" --semantic 0.7 --lexical 0.3 > resultados_simple.json
python3 ../solr2trec.py --run-id weight_0.5_0.5 < resultados_simple.json > results_sys2_semantic_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec1.txt
./../src/trec_eval/trec_eval qrels_trec1.txt results_sys2_semantic_trec.txt
# cat results_sys2_semantic_trec.txt | python3 ../plot_pr.py --qrels qrels_trec1.txt --output prec_rec_sys2_semantic.png

# 0.3 semantic 0.7 lexical
python3 ../M3/mix_querys.py --query "persistent fatigue exhaustion" --semantic 0.3 --lexical 0.7 > resultados_simple.json
python3 ../solr2trec.py --run-id weight_0.5_0.5 < resultados_simple.json > results_sys3_semantic_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec1.txt
./../src/trec_eval/trec_eval qrels_trec1.txt results_sys3_semantic_trec.txt
# cat results_sys3_semantic_trec.txt | python3 ../plot_pr.py --qrels qrels_trec1.txt --output prec_rec_sys3_semantic.png

# 0.0 semantic 1.0 lexical
python3 ../M3/mix_querys.py --query "persistent fatigue exhaustion" --semantic 0.0 --lexical 1.0 > resultados_simple.json
python3 ../solr2trec.py --run-id weight_0.5_0.5 < resultados_simple.json > results_sys4_semantic_trec.txt
cat qrels.txt | python3 ../qrels2trec.py > qrels_trec4.txt
./../src/trec_eval/trec_eval qrels_trec4.txt results_sys4_semantic_trec.txt
# cat results_sys4_semantic_trec.txt | python3 ../plot_pr.py --qrels qrels_trec4.txt --output prec_rec_sys1_semantic.png

# Figure all systems
python3 ../plot_pr_n.py \
  --qrels qrels_trec1.txt qrels_trec2.txt qrels_trec3.txt \
  --results results_sys1_semantic_trec.txt results_sys2_semantic_trec.txt results_sys3_semantic_trec.txt \
  --labels "System 1" "System 2" "System 3" \
  --output prec_rec_sys_all_semantic.png

rm resultados_simple.json resultados_boosted.json resultados_weights.json