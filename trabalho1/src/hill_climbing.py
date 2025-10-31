from typing import Dict, Any, Tuple
import time
import random
from eight_queens_representation import EightQueensProblem, Board


# ====================================================================
# FUNÇÃO PRINCIPAL DE HILL CLIMBING
# ====================================================================

def hill_climbing_search(
        problem: EightQueensProblem,
        initial_board: Board,
        max_sideway_moves: int = 0
) -> Dict[str, Any]:
    """
    Implementa a Busca Hill Climbing (Subida de Encosta) com ou sem movimentos laterais.

    :param max_sideway_moves: Limite de movimentos laterais (custo igual ao atual). 0 = Sem laterais.
    """
    start_time = time.time()

    current_board = initial_board
    current_conflicts = problem.conflicts(current_board)
    sideway_moves_count = 0
    steps = 0

    while True:
        steps += 1

        if current_conflicts == 0:
            break

        # 1. Encontra o melhor vizinho (menor conflito)
        neighbors_info = []
        for move, neighbor_board in problem.neighbors(current_board):
            conflicts = problem.conflicts(neighbor_board)
            neighbors_info.append((conflicts, neighbor_board))

        # Se não houver vizinhos (teoricamente impossível no 8 Queens), para.
        if not neighbors_info:
            break

        min_conflicts = min(c for c, b in neighbors_info)
        best_neighbors = [b for c, b in neighbors_info if c == min_conflicts]

        # 2. Decisão de Movimento

        # Máximo Local: Se o melhor vizinho for pior que o estado atual
        if min_conflicts > current_conflicts:
            break

            # Escolhe aleatoriamente um dos melhores vizinhos (para quebrar empates)
        next_board = random.choice(best_neighbors)
        next_conflicts = min_conflicts

        if next_conflicts == current_conflicts:
            # Movimento Lateral: Apenas se permitido e dentro do limite
            if sideway_moves_count < max_sideway_moves:
                sideway_moves_count += 1
                current_board = next_board
                current_conflicts = next_conflicts
            else:
                # Limite lateral atingido -> Máximo Local
                break
        else:  # next_conflicts < current_conflicts (Movimento de Subida)
            sideway_moves_count = 0  # Reseta o contador
            current_board = next_board
            current_conflicts = next_conflicts

    end_time = time.time()

    return {
        'board_final': current_board,
        'conflicts_final': current_conflicts,
        'sucesso': current_conflicts == 0,
        'passos_totais': steps,
        'tempo_execucao': end_time - start_time,
        'movimentos_laterais': sideway_moves_count,
    }


# ====================================================================
# FUNÇÃO DE RANDOM RESTART HILL CLIMBING
# ====================================================================

def random_restart_hill_climbing(
        problem: EightQueensProblem,
        max_restarts: int,
        max_sideway_moves: int = 0
) -> Dict[str, Any]:
    """
    Implementa o Hill Climbing com Reinício Aleatório (Random-Restart).
    """
    start_time = time.time()

    restarts_count = 0
    total_steps = 0

    # Roda a busca até o sucesso ou atingir o limite de reinícios
    while restarts_count <= max_restarts:

        # Gera novo estado inicial aleatório para cada tentativa
        initial_board = problem.initial_board()

        result = hill_climbing_search(problem, initial_board, max_sideway_moves)
        total_steps += result['passos_totais']

        if result['sucesso']:
            end_time = time.time()
            return {
                'algoritmo': f'HC Reinício Aleatório (Laterais: {max_sideway_moves})',
                'sucesso': True,
                'board_final': result['board_final'],
                'conflitos_final': 0,
                'tempo_execucao': end_time - start_time,
                'reinicios_totais': restarts_count,
                'passos_acumulados': total_steps,
            }

        restarts_count += 1

    # Falha (limite de reinícios atingido)
    end_time = time.time()
    return {
        'algoritmo': f'HC Reinício Aleatório (Laterais: {max_sideway_moves})',
        'sucesso': False,
        'board_final': result['board_final'] if 'result' in locals() else None,
        'conflitos_final': result['conflicts_final'] if 'result' in locals() else -1,
        'tempo_execucao': end_time - start_time,
        'reinicios_totais': max_restarts,
        'passos_acumulados': total_steps,
    }