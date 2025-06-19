#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np


def calculate_precision_recall(qrels_file, results_file):
    """
    Calcula precision, recall e métricas relacionadas para um qrels e arquivo de resultados fornecidos.
    """
    # Ler qrels (ground truth) do ficheiro
    with open(qrels_file, "r") as f:
        y_true = {line.strip().split()[2] for line in f}  # IDs relevantes como conjunto (set)

    # Ler predições do ficheiro de resultados
    with open(results_file, "r") as f:
        y_pred = [line.strip().split()[2] for line in f]  # IDs preditos do formato TREC

    # Verificar inputs vazios
    if not y_pred or not y_true:
        print(f"Erro: qrels ({qrels_file}) ou resultados ({results_file}) estão vazios.")
        return None

    # Cálculo de precision, recall, MAP e ranks relevantes
    precision = []
    recall = []
    relevant_ranks = []
    relevant_count = 0

    for i in range(1, len(y_pred) + 1):
        if y_pred[i - 1] in y_true:
            relevant_count += 1
            relevant_ranks.append(relevant_count / i)

        precision.append(relevant_count / i)
        recall.append(relevant_count / len(y_true))

    map_score = np.sum(relevant_ranks) / len(y_true) if relevant_ranks else 0

    recall_levels = np.linspace(0.0, 1.0, 11)
    interpolated_precision = [
        max([p for p, r in zip(precision, recall) if r >= r_level], default=0)
        for r_level in recall_levels
    ]

    auc_score = np.trapz(interpolated_precision, recall_levels)

    return recall_levels, interpolated_precision, map_score, auc_score


def main(qrels_files, results_files, labels, output_file):
    """
    Gera um gráfico de Precision-Recall com múltiplas linhas (uma por cada sistema).

    Arguments:
        qrels_files -- Lista de ficheiros de qrels (ground truth) em formato TREC.
        results_files -- Lista de ficheiros de resultados preditos em formato TREC.
        labels -- Lista de labels associadas a cada linha no gráfico.
        output_file -- Nome do ficheiro PNG para guardar o gráfico.
    """
    # Verificar se o número de qrels, resultados e labels está correto
    if len(qrels_files) != len(results_files) or len(qrels_files) != len(labels):
        print("Erro: O número de ficheiros qrels, resultados e labels deve ser o mesmo.")
        return

    # Processar cada sistema e plotar a sua linha no gráfico
    for qrels_file, results_file, label in zip(qrels_files, results_files, labels):
        results = calculate_precision_recall(qrels_file, results_file)
        if results is None:
            continue

        recall_levels, interpolated_precision, map_score, auc_score = results
        plt.plot(
            recall_levels,
            interpolated_precision,
            drawstyle="steps-post",
            label=f"{label} (MAP: {map_score:.4f}, AUC: {auc_score:.4f})",
            linewidth=1,
        )

    # Personalizar o gráfico
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})
    plt.title("Precision-Recall Curve")

    # Guardar o gráfico
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Gráfico Precision-Recall guardado como {output_file}")


if __name__ == "__main__":
    # Argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description="Gera um gráfico de Precision-Recall com múltiplas linhas (múltiplos sistemas)."
    )
    parser.add_argument(
        "--qrels",
        type=str,
        nargs="+",  # Permite múltiplos ficheiros qrels
        required=True,
        help="Lista de caminhos para os ficheiros qrels (ground truth) em formato TREC.",
    )
    parser.add_argument(
        "--results",
        type=str,
        nargs="+",  # Permite múltiplos ficheiros de resultados
        required=True,
        help="Lista de caminhos para os ficheiros de resultados preditos em formato TREC.",
    )
    parser.add_argument(
        "--labels",
        type=str,
        nargs="+",  # Permite múltiplas labels
        required=True,
        help="Lista de labels para as linhas do gráfico (uma para cada sistema).",
    )
    parser.add_argument("--output", type=str, required=True, help="Caminho para o ficheiro PNG de saída.")
    args = parser.parse_args()

    # Chamar a função principal
    main(args.qrels, args.results, args.labels, args.output)
