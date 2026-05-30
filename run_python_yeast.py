import sys
import time
import types
import random
import argparse
import statistics
from pathlib import Path

import pandas as pd


# O numba nao e usado pelo algoritmo, mas o import no arquivo original quebra
# com a versao atual do NumPy instalada neste ambiente.
numba_stub = types.ModuleType("numba")
numba_stub.jit = lambda *args, **kwargs: (
    args[0] if args and callable(args[0]) else (lambda fn: fn)
)
numba_stub.cuda = None
sys.modules["numba"] = numba_stub

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


def output_for_seed(output_path, seed):
    path = Path(output_path)
    if path.suffix:
        return path.with_name(f"{path.stem}_seed{seed}{path.suffix}")
    return path.with_name(f"{path.name}_seed{seed}.csv")


def standard_deviation(values):
    if len(values) <= 1:
        return 0.0
    return statistics.stdev(values)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa o ACO guloso Python em multiplas seeds."
    )
    parser.add_argument("--input", default="dataset/yeast.csv")
    parser.add_argument("--target", default="name")
    parser.add_argument("--output", default="dataset/yeast_reduzido_python.csv")
    parser.add_argument("--seeds", type=parse_seeds, default=DEFAULT_SEEDS)
    parser.add_argument("--initial-pheromone", type=float, default=1.0)
    parser.add_argument("--evaporation-rate", type=float, default=0.1)
    parser.add_argument("--q", type=float, default=1.0)
    return parser.parse_args()


def main():
    args = parse_args()

    experiment_start = time.perf_counter()

    load_start = time.perf_counter()
    original_df = pd.read_csv(args.input)
    dataframe = pd.read_csv(args.input)
    classes = dataframe[args.target]
    dataframe = dataframe.drop(columns=[args.target])
    x_values = dataframe.to_numpy()
    y_values = classes.to_numpy()
    load_seconds = time.perf_counter() - load_start

    results = []

    print(f"Arquivo: {args.input}")
    print(
        f"Instancias: {len(original_df)} | "
        f"Atributos: {dataframe.shape[1]} | Alvo: {args.target}"
    )
    print(
        "Parametros: "
        f"feromonio inicial={args.initial_pheromone:g} | "
        f"evaporacao={args.evaporation_rate:g} | Q={args.q:g}"
    )
    print(f"Tempo carregamento CSV: {load_seconds:.6f} segundos")
    print(f"Seeds: {', '.join(str(seed) for seed in args.seeds)}")
    print("Iniciando execucoes Python")

    for seed in args.seeds:
        output_path = output_for_seed(args.output, seed)

        random.seed(seed)
        search_start = time.perf_counter()
        indices_selected = guloso.run_colony(
            x_values,
            y_values,
            initial_pheromone=args.initial_pheromone,
            evaporarion_rate=args.evaporation_rate,
            Q=args.q,
        )
        search_seconds = time.perf_counter() - search_start

        write_start = time.perf_counter()
        reduced_dataframe = original_df.iloc[indices_selected]
        reduced_dataframe.to_csv(output_path, index=False)
        write_seconds = time.perf_counter() - write_start

        total_seed_seconds = search_seconds + write_seconds
        results.append(
            {
                "seed": seed,
                "selected": len(indices_selected),
                "search_seconds": search_seconds,
                "write_seconds": write_seconds,
                "total_seed_seconds": total_seed_seconds,
                "output_path": output_path,
            }
        )

        print(
            f"Seed {seed}: selecionadas={len(indices_selected)} | "
            f"run_colony={search_seconds:.6f}s | "
            f"escrita={write_seconds:.6f}s | "
            f"total_seed={total_seed_seconds:.6f}s | "
            f"saida={output_path}"
        )

    search_times = [result["search_seconds"] for result in results]
    total_seed_times = [result["total_seed_seconds"] for result in results]
    selected_counts = [result["selected"] for result in results]
    experiment_seconds = time.perf_counter() - experiment_start

    print("\nResumo Python")
    print(f"Execucoes: {len(results)}")
    print(f"Tempo medio run_colony: {statistics.mean(search_times):.6f} segundos")
    print(
        "Desvio padrao run_colony: "
        f"{standard_deviation(search_times):.6f} segundos"
    )
    print(
        "Tempo medio total por seed: "
        f"{statistics.mean(total_seed_times):.6f} segundos"
    )
    print(
        "Desvio padrao total por seed: "
        f"{standard_deviation(total_seed_times):.6f} segundos"
    )
    print(
        "Instancias selecionadas media: "
        f"{statistics.mean(selected_counts):.2f}"
    )
    print(f"Tempo total do experimento: {experiment_seconds:.6f} segundos")


if __name__ == "__main__":
    main()
