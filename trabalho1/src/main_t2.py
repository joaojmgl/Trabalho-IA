import time
from eight_queens_representation import EightQueensProblem, Board
from hill_climbing import hill_climbing_search, random_restart_hill_climbing
from typing import Dict, Any, List
import random
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE IMPRESSÃO/PLOTAGEM
# ----------------------------------------------------------------------

def print_board(board: Board):
    """Imprime o tabuleiro de forma visual."""
    if not board:
        return

    N = len(board)
    print("  " + "---" * N)
    for r in range(N):
        row_str = f"{N - 1 - r}|"
        for c in range(N):
            # A linha (row) é N - 1 - r, pois r=0 é o topo (linha N-1)
            if board[c] == N - 1 - r:
                row_str += " Q "
            else:
                row_str += " . "
        print(row_str + "|")
    print("  " + "---" * N)
    print("   " + " ".join(str(c) for c in range(N)))


def plot_success_rate(results: Dict[str, Any]):
    """Gera um gráfico de barras para a Taxa de Sucesso e salva como PNG."""
    names = list(results.keys())
    success_rates = [r['taxa_sucesso'] * 100 for r in results.values()]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, success_rates, color=['skyblue', 'lightcoral', 'lightgreen', 'gold'])

    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Taxa de Sucesso do Hill Climbing (8 Rainhas)')
    plt.ylim(0, 100)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("taxa_sucesso_8rainhas.png")
    plt.close()  # Fecha a figura para economizar memória
    print("\nGráfico 'taxa_sucesso_8rainhas.png' salvo.")


# ----------------------------------------------------------------------
# FUNÇÃO DE EXECUÇÃO E COMPARAÇÃO
# ----------------------------------------------------------------------

def run_queens_comparison(num_runs: int = 100, max_restarts: int = 50, lateral_limit: int = 10):
    """Executa e compara as variações do Hill Climbing."""

    problem = EightQueensProblem()
    results: Dict[str, Dict[str, Any]] = {}

    # Define as variações a serem testadas:
    test_configurations = {
        "HC Simples": {
            "search_func": hill_climbing_search,
            "lateral": 0, "restarts": 0,
            "is_rr": False,
            "description": "Hill Climbing (HC) sem laterais, sem reinício."
        },
        "HC Lateral": {
            "search_func": hill_climbing_search,
            "lateral": lateral_limit, "restarts": 0,
            "is_rr": False,
            "description": f"HC com laterais (limite={lateral_limit}), sem reinício."
        },
        "HC Random Restart Simples": {
            "search_func": random_restart_hill_climbing,
            "lateral": 0, "restarts": max_restarts,
            "is_rr": True,
            "description": f"HC com Reinício Aleatório (máx {max_restarts}), sem laterais."
        },
        "HC Random Restart Lateral": {
            "search_func": random_restart_hill_climbing,
            "lateral": lateral_limit, "restarts": max_restarts,
            "is_rr": True,
            "description": f"HC com Reinício Aleatório (máx {max_restarts}), laterais={lateral_limit}."
        },
    }

    print("\n=======================================================")
    print(f"Executando comparação do Hill Climbing ({num_runs} iterações por configuração)")
    print("=======================================================\n")

    for name, config in test_configurations.items():
        success_count = 0
        total_steps = 0
        total_restarts = 0

        print(f"--- Rodando {name}: {config['description']} ---")

        start_time_total = time.time()

        # Roda o teste 'num_runs' vezes
        # Roda o teste 'num_runs' vezes
        for _ in range(num_runs):

            if config['is_rr']:
                # Random Restart HC
                metrics = config["search_func"](problem, config['restarts'], config['lateral'])
            else:
                # HC Simples ou Lateral (Roda uma vez, cada run começa de um board inicial)
                initial_board = problem.initial_board()
                metrics = config["search_func"](problem, initial_board, config['lateral'])

            if metrics['sucesso']:
                success_count += 1

                # CORREÇÃO: Usamos a flag 'is_rr' para acessar a chave correta diretamente.
                if config['is_rr']:
                    # Runs com Reinício Aleatório usam 'passos_acumulados'
                    total_steps += metrics['passos_acumulados']
                else:
                    # Runs Simples/Lateral usam 'passos_totais'
                    total_steps += metrics['passos_totais']

                total_restarts += metrics.get('reinicios_totais', 0)

        end_time_total = time.time()

        taxa_sucesso = success_count / num_runs
        avg_steps = total_steps / success_count if success_count > 0 else 0
        avg_restarts = total_restarts / success_count if success_count > 0 else 0

        results[name] = {
            'taxa_sucesso': taxa_sucesso,
            'tempo_total_execucao': end_time_total - start_time_total,
            'media_passos_sucesso': avg_steps,
            'media_reinicios_sucesso': avg_restarts,
            'runs': num_runs
        }

        print(f"  > Taxa de Sucesso: {taxa_sucesso:.2f}")
        if success_count > 0:
            print(f"  > Média de Passos (Sucesso): {avg_steps:.1f}")
            print(f"  > Média de Reinícios (Sucesso): {avg_restarts:.1f}")
        else:
            print("  > Não houve sucesso para calcular as médias.")
        print("-" * 30)

    # Geração da Tabela de Comparação
    print("\n\n=======================================================")
    print("TABELA DE COMPARAÇÃO DE HILL CLIMBING (8 RAINHAS)")
    print("=======================================================")

    header = f"{'Configuração':<30} | {'Taxa Sucesso (%)':<18} | {'Avg Reinícios':<13} | {'Avg Passos':<10}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    for name, metrics in results.items():
        row = (
            f"{name:<30} | "
            f"{metrics['taxa_sucesso'] * 100:<18.2f} | "
            f"{metrics['media_reinicios_sucesso']:<13.1f} | "
            f"{metrics['media_passos_sucesso']:<10.1f}"
        )
        print(row)

    print(separator)

    # Gerar gráfico
    try:
        plot_success_rate(results)
    except Exception as e:
        print(f"\nAVISO: Não foi possível gerar o gráfico. Certifique-se de que 'matplotlib' está instalado. Erro: {e}")

    # Exemplo de solução (se houver)
    print("\n--- Exemplo de Solução (Qualquer execução) ---")
    final_result = random_restart_hill_climbing(problem, 100, 10)
    if final_result['sucesso']:
        print("Solução encontrada no último teste:")
        print_board(final_result['board_final'])
    else:
        print("Nenhuma solução foi encontrada no último teste.")


# ----------------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Garante que as execuções sejam determinísticas (se desejado)
    random.seed(42)

    run_queens_comparison(num_runs=100, max_restarts=50, lateral_limit=10)