import argparse
import statistics
import time
from pathlib import Path

import numpy as np
import pandas as pd

import GulosoComplexity as guloso

DEFAULT_SEEDS = [0, 42, 123, 789, 1024]


def parse_seeds(value):
    seeds = []
    for item in value.split(","):
        item = item.strip()
        if item:
            seeds.append(int(item))
    if not seeds:
        raise argparse.ArgumentTypeError("informe pelo menos uma seed")
    return seeds


def output_for_seed(output_path, seed, multiple):
    path = Path(output_path)
    if not multiple:
        return path
    if path.suffix:
        return path.with_name(f"{path.stem}_seed{seed}{path.suffix}")
    return path.with_name(f"{path.name}_seed{seed}.csv")


def standard_deviation(values):
    if len(values) <= 1:
        return 0.0
    return statistics.stdev(values)


def encode_features(dataframe: pd.DataFrame) -> np.ndarray:
    """Converte cada coluna para float; colunas nao-numericas (categoricas) sao
    codificadas como inteiros na ordem de primeira aparicao, igual ao
    string_map_get_or_add usado nas versoes C/CUDA."""
    columns = []
    for col in dataframe.columns:
        series = dataframe[col]
        numeric = pd.to_numeric(series, errors="coerce")
        if numeric.isna().any():
            codes, _ = pd.factorize(series, sort=False)
            columns.append(codes.astype(np.float64))
        else:
            columns.append(numeric.to_numpy(dtype=np.float64))
    return np.column_stack(columns)


def resolve_target_column(columns, target_arg):
    if target_arg is None:
        return columns[-1]
    if target_arg in columns:
        return target_arg
    try:
        index = int(target_arg)
    except ValueError:
        raise SystemExit(f"Erro: coluna alvo '{target_arg}' nao encontrada.")
    if 1 <= index <= len(columns):
        return columns[index - 1]
    if 0 <= index < len(columns):
        return columns[index]
    raise SystemExit(f"Erro: coluna alvo '{target_arg}' nao encontrada.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa o ACO guloso (Python/numpy vetorizado) em multiplas seeds."
    )
    parser.add_argument("--input", default="dataset/yeast.csv")
    parser.add_argument("--target", default=None)
    parser.add_argument("--output", default="dataset/yeast_reduzido_python.csv")
    parser.add_argument("--seeds", type=parse_seeds, default=DEFAULT_SEEDS)
    parser.add_argument("--initial-pheromone", type=float, default=1.0)
    parser.add_argument("--evaporation-rate", type=float, default=0.1)
    parser.add_argument("--q", type=float, default=1.0)
    return parser.parse_args()


def main():
    args = parse_args()

    experiment_start = time.perf_counter()

    original_df = pd.read_csv(args.input)
    target = resolve_target_column(list(original_df.columns), args.target)
    dataframe = original_df.drop(columns=[target])
    x_values = encode_features(dataframe)
    y_values = original_df[target].to_numpy()

    print(f"Arquivo: {args.input}")
    print(
        f"Instancias: {len(original_df)} | Atributos: {dataframe.shape[1]} | "
        f"Alvo: {target}"
    )
    print(
        "Parametros: "
        f"feromonio inicial={args.initial_pheromone:g} | "
        f"evaporacao={args.evaporation_rate:g} | Q={args.q:g}"
    )
    print("Seeds: " + ", ".join(str(seed) for seed in args.seeds))
    print("Iniciando execucoes Python")

    run_times = []
    total_seed_times = []
    selected_counts = []
    multiple = len(args.seeds) > 1

    for seed in args.seeds:
        output_path = output_for_seed(args.output, seed, multiple)

        print(f"\nSeed {seed}")
        rng = np.random.default_rng(seed)
        run_start = time.perf_counter()
        indices_selected, accuracy, aco_seconds, knn_seconds = guloso.run_colony(
            x_values,
            y_values,
            initial_pheromone=args.initial_pheromone,
            evaporation_rate=args.evaporation_rate,
            Q=args.q,
            rng=rng,
        )
        run_seconds = time.perf_counter() - run_start

        reduced_dataframe = original_df.iloc[indices_selected]
        reduced_dataframe.to_csv(output_path, index=False)
        total_seed_seconds = time.perf_counter() - run_start

        run_times.append(run_seconds)
        total_seed_times.append(total_seed_seconds)
        selected_counts.append(len(indices_selected))

        print(f"Instancias selecionadas: {len(indices_selected)}")
        print(f"Acuracia 1-NN da melhor solucao: {accuracy:.6f}")
        print(f"Tempo ACO: {aco_seconds:.6f} segundos")
        print(f"Tempo avaliacao 1-NN: {knn_seconds:.6f} segundos")
        print(f"Tempo run_colony: {run_seconds:.6f} segundos")
        print(f"Tempo total seed: {total_seed_seconds:.6f} segundos")
        print(f"CSV reduzido salvo em: {output_path}")

    experiment_seconds = time.perf_counter() - experiment_start

    print("\nResumo Python")
    print(f"Execucoes: {len(args.seeds)}")
    print(f"Tempo medio run_colony: {statistics.mean(run_times):.6f} segundos")
    print(f"Desvio padrao run_colony: {standard_deviation(run_times):.6f} segundos")
    print(f"Tempo medio total por seed: {statistics.mean(total_seed_times):.6f} segundos")
    print(f"Desvio padrao total por seed: {standard_deviation(total_seed_times):.6f} segundos")
    print(f"Instancias selecionadas media: {statistics.mean(selected_counts):.2f}")
    print(f"Tempo total do experimento: {experiment_seconds:.6f} segundos")


if __name__ == "__main__":
    main()
