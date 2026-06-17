import time

import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

# Ordem de complexidade da abordagem gulosa O(num_ants x num_instances^2 * iterations)
# Versao vetorizada com numpy: a mesma logica da versao original (formiga escolhe na
# ordem de feromonio, sorteio binario por candidato, deposito recalculado sobre o
# caminho inteiro a cada rodada, evaporacao global), mas sem laços Python aninhados
# O(n^2), para ficar comparavel em escala com as versoes C/CUDA.


def get_pairwise_distance(matrix: np.ndarray) -> np.ndarray:
    return euclidean_distances(matrix)


def create_colony(num_ants: int) -> np.ndarray:
    colony = np.full((num_ants, num_ants), -1, dtype=np.int8)
    np.fill_diagonal(colony, 1)
    return colony


def create_pheromone_trails(n: int, initial_pheromone: float) -> np.ndarray:
    trails = np.full((n, n), initial_pheromone, dtype=np.float64)
    np.fill_diagonal(trails, 0.0)
    return trails


def choose_paths_greedy_round(colony, pheromone, distances, last_pos, undefined_count,
                               path_from, path_to, path_lengths, tour_length, rng):
    """Processa uma rodada do ACO guloso para todas as formigas ainda ativas.

    Cada formiga tenta os candidatos disponiveis em ordem decrescente de
    feromonio (a partir da posicao atual), sorteando um bit por candidato;
    aceita o primeiro candidato sorteado com 1 e rejeita (marca 0) os demais
    ja testados nesta rodada. Retorna quantas posicoes deixaram de ser -1.
    """
    n = colony.shape[0]
    consumed_total = 0

    for i in range(n):
        if undefined_count[i] == 0:
            continue

        avail = np.nonzero(colony[i] < 0)[0]
        if avail.size == 0:
            undefined_count[i] = 0
            continue

        pher_vals = pheromone[last_pos[i], avail]
        order = pher_vals.argsort()[::-1]
        avail_sorted = avail[order]

        bits = rng.integers(0, 2, size=avail_sorted.size)
        ones = np.flatnonzero(bits)

        if ones.size > 0:
            accept_pos = ones[0]
            if accept_pos > 0:
                colony[i, avail_sorted[:accept_pos]] = 0
            accepted = avail_sorted[accept_pos]
            colony[i, accepted] = 1

            length = path_lengths[i]
            path_from[i, length] = last_pos[i]
            path_to[i, length] = accepted
            path_lengths[i] = length + 1
            tour_length[i] += distances[last_pos[i], accepted]
            last_pos[i] = accepted

            consumed = accept_pos + 1
        else:
            colony[i, avail_sorted] = 0
            consumed = avail_sorted.size

        undefined_count[i] -= consumed
        consumed_total += consumed

    return consumed_total


def update_pheromones(pheromone, path_from, path_to, path_lengths, tour_length, q,
                       evaporation_rate):
    n = pheromone.shape[0]
    deposit = np.divide(q, tour_length, out=np.zeros(n), where=tour_length > 0)

    for i in range(n):
        length = path_lengths[i]
        if length > 1:
            pheromone[path_from[i, 1:length], path_to[i, 1:length]] += deposit[i]

    pheromone *= (1.0 - evaporation_rate)


def evaluate_solutions_1nn(colony: np.ndarray, distances: np.ndarray, y: np.ndarray):
    n = colony.shape[0]
    best_ant = -1
    best_correct = -1

    for i in range(n):
        selected_idx = np.nonzero(colony[i] != 0)[0]
        if selected_idx.size == 0:
            continue
        sub = distances[:, selected_idx]
        nearest_local = sub.argmin(axis=1)
        predicted = y[selected_idx[nearest_local]]
        correct = int(np.count_nonzero(predicted == y))
        if correct > best_correct:
            best_correct = correct
            best_ant = i

    selected_indices = np.nonzero(colony[best_ant] != 0)[0]
    accuracy = best_correct / n
    return selected_indices, accuracy


def run_colony(X: np.ndarray, Y: np.ndarray, initial_pheromone: float,
               evaporation_rate: float, Q: float, rng: np.random.Generator):
    """Executa o ACO guloso e retorna (indices_selecionados, acuracia, tempo_aco, tempo_1nn)."""
    n = X.shape[0]
    distances = get_pairwise_distance(X)
    pheromone = create_pheromone_trails(n, initial_pheromone)
    colony = create_colony(n)

    path_from = np.empty((n, n), dtype=np.int32)
    path_to = np.empty((n, n), dtype=np.int32)
    path_lengths = np.ones(n, dtype=np.int64)
    path_from[:, 0] = np.arange(n)
    path_to[:, 0] = np.arange(n)
    tour_length = np.zeros(n, dtype=np.float64)
    last_pos = np.arange(n)
    undefined_count = np.full(n, n - 1, dtype=np.int64)
    remaining_unknown = n * n - n

    aco_start = time.perf_counter()
    iteration = 0
    while remaining_unknown > 0:
        iteration += 1
        consumed = choose_paths_greedy_round(
            colony, pheromone, distances, last_pos, undefined_count,
            path_from, path_to, path_lengths, tour_length, rng,
        )
        remaining_unknown -= consumed

        update_pheromones(pheromone, path_from, path_to, path_lengths, tour_length, Q,
                           evaporation_rate)

        if iteration % 100 == 0 or remaining_unknown == 0:
            print(f"Iteracao {iteration} concluida; posicoes indefinidas restantes: {remaining_unknown}")
    aco_seconds = time.perf_counter() - aco_start

    knn_start = time.perf_counter()
    selected_indices, accuracy = evaluate_solutions_1nn(colony, distances, Y)
    knn_seconds = time.perf_counter() - knn_start

    return selected_indices, accuracy, aco_seconds, knn_seconds
