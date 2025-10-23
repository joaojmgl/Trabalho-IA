# main.py
# Ponto de execução principal para o Trabalho 1: Busca no Labirinto.
import os
from maze_representation import Maze
from search import (
    bfs_search, dfs_search, ucs_search,
    greedy_search, astar_search, # Manhattan
    greedy_chebyshev_search, astar_chebyshev_search # Chebyshev
)
from typing import Dict, Any
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------
# 1. FUNÇÃO DE GERAÇÃO DO LABIRINTO DE TESTE
# ----------------------------------------------------------------------

# def create_sample_maze_file(filename="labirinto.txt"):
#     """Cria um arquivo de labirinto de exemplo para o teste."""
#     maze_content = (
#         "S.....#.\n"
#         ".###..#.\n"
#         "..#...#.\n"
#         ".#.#..#.\n"
#         "...#G.#.\n"
#     )
#
#
#     maze_content_v2 = (
#         "S.....#.\n"
#         ".###..#.\n"
#         "..#...#.\n"
#         ".#.#..#.\n"
#         "...#G.#.\n"
#     )
#
#     if not os.path.exists(filename):
#         with open(filename, 'w') as f:
#             f.write(maze_content_v2)
#         print(f"Arquivo '{filename}' criado com labirinto de teste.")
#     else:
#         print(f"Arquivo '{filename}' já existe, usando existente.")
#

# ----------------------------------------------------------------------
# 2. FUNÇÃO DE GERAÇÃO DE GRAFOS
# ----------------------------------------------------------------------

def plot_maze_search(maze: Maze, metrics: Dict[str, Any], save_path: str = None):
    H, W = maze.H, maze.W

    # 1. Cria a matriz base de cores
    # 0: Livre (Branco/Cinza Claro), 1: Parede (Preto), 2: Início/Fim
    plot_data = np.zeros((H, W))
    for r in range(H):
        for c in range(W):
            if maze.grid[r][c] == '#':
                plot_data[r, c] = 1 # Parede

    # Define o mapa de cores
    cmap = plt.cm.get_cmap('YlGnBu') # Um bom mapa de cores para visualização
    cmap.set_bad(color='black')

    fig, ax = plt.subplots(figsize=(W * 0.5, H * 0.5))


    expanded_positions = metrics.get('nos_expandidos_posicoes', [])

    expansion_map = np.copy(plot_data)
    expansion_order = 2

    for r, c in expanded_positions:
        if expansion_map[r, c] == 0:
             expansion_map[r, c] = expansion_order
             expansion_order += 1

    max_val = max(2, expansion_order)

    masked_data = np.ma.masked_where(plot_data == 1, expansion_map)

    im = ax.imshow(masked_data, cmap=cmap, vmin=0, vmax=max_val)

    solution_path = metrics.get('caminho', [])
    path_color = 'red'

    if solution_path:
        path_rows, path_cols = zip(*solution_path)
        ax.plot(path_cols, path_rows, marker='o', markersize=4, linestyle='-',
                color=path_color, linewidth=2, label='Caminho Solução', zorder=5)

    start_row, start_col = maze.start
    goal_row, goal_col = maze.goal

    ax.plot(start_col, start_row, 's', markersize=10, color='lime', label='Início (S)', zorder=10)
    ax.plot(goal_col, goal_row, '*', markersize=10, color='gold', label='Objetivo (G)', zorder=10)

    # 5. Formatação
    ax.set_title(f"{metrics['algoritmo']} - Custo: {metrics['custo_total']:.0f} | Nós Exp: {metrics['nos_expandidos']}", fontsize=10)
    ax.set_xticks(np.arange(W))
    ax.set_yticks(np.arange(H))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0) # Remove as marcas do tick
    ax.grid(color='gray', linestyle='-', linewidth=0.5)

    # Inverte o eixo Y para o (0,0) ficar no canto superior esquerdo
    ax.invert_yaxis()

    # 6. Salvar ou Mostrar
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close(fig)
    else:
        plt.show()




# ----------------------------------------------------------------------
# 3. FUNÇÃO DE EXECUÇÃO E COMPARAÇÃO
# ----------------------------------------------------------------------

def run_all_searches(maze: Maze):
    
    # Algoritmos a serem executados: 2 Não Informados (BFS, UCS) e 2 Informados (Greedy, A*)
    search_algorithms = {
        "BFS               ": bfs_search,
        "DFS               ": dfs_search,
        "UCS               ": ucs_search,
        "GREEDY (Manhattan)": greedy_search,
        "A* (Manhattan)    ": astar_search,
        "GREEDY (Chebyshev)": greedy_chebyshev_search,  # NOVA BUSCA
        "A* (Chebyshev)    ": astar_chebyshev_search,  # NOVA BUSCA
    }
    
    results = {}
    
    print("\n=======================================================")
    print(f"Executando buscas no labirinto de {maze.H}x{maze.W}")
    print(f"Início: {maze.start}, Objetivo: {maze.goal}")
    print("=======================================================\n")
    
    for name, func in search_algorithms.items():
        print(f"--- Executando {name} ---")
        try:
            metrics = func(maze)
            results[name] = metrics
            
            print(f"  > Sucesso: {metrics['sucesso']}")
            if metrics['sucesso']:
                print(f"  > Custo Total: {metrics['custo_total']:.2f}")
                print(f"  > Nós Expandidos: {metrics['nos_expandidos']}")
                print(f"  > Memória Máxima: {metrics['memoria_maxima']}")
                print(f"  > Optimalidade: {metrics['optimalidade']}")
                print(f"  > Gerando gráfico: {name.replace(' ', '_').replace('*', 'star')}.png")
                save_filename = f"../data/{name.replace(' ', '_').replace('*', 'star').replace('(', '').replace(')', '')}_mapa.png"
                plot_maze_search(maze, metrics, save_path=save_filename)
            else:
                print("  > Solução não encontrada.")
            print("-" * 30)

        except Exception as e:
            print(f"ERRO ao executar {name}: {e}")
            print("-" * 30)

    print("\n\n=======================================================")
    print("TABELA DE COMPARAÇÃO DE ALGORITMOS (MÉTRICAS)")
    print("=======================================================")
    
    header = f"{'Algoritmo':<18} | {'Sucesso':<7} | {'Ótimo':<5} | {'Custo':<8} | {'Nós Expandidos':<16} | {'Memória Máx':<13} | {'Tempo (s)':<10}"
    separator = "-" * len(header)
    print(header)
    print(separator)
    
    for name, metrics in results.items():
        tempo_str = f"{metrics['tempo_execucao']:.4f}" if metrics['tempo_execucao'] < 1 else f"{metrics['tempo_execucao']:.2f}"
        
        row = (
            f"{name:<10} | "
            f"{'SIM' if metrics['sucesso'] else 'NÃO':<7} | "
            f"{'SIM' if metrics['optimalidade'] else 'NÃO':<5} | "
            f"{metrics['custo_total']:<8.2f} | "
            f"{metrics['nos_expandidos']:<16} | "
            f"{metrics['memoria_maxima']:<13} | "
            f"{tempo_str:<10}"
        )
        print(row)
        
    print(separator)
    print("\nCaminho da Solução A* (Manhattan): ", results.get("A* (Manhattan)    ", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução A* (Chebyshev): ", results.get("A* (Chebyshev)    ", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução GREEDY (Manhattan): ", results.get("GREEDY (Manhattan)", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução GREEDY (Chebyshev): ", results.get("GREEDY (Chebyshev)", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução BFS: ", results.get("BFS               ", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução DFS: ", results.get("DFS               ", {}).get("caminho", "Não encontrado"))
    print("\nCaminho da Solução UCS: ", results.get("UCS               ", {}).get("caminho", "Não encontrado"))


# ----------------------------------------------------------------------
# 4. EXECUÇÃO PRINCIPAL
# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    # create_sample_maze_file()
    
    try:
        maze_instance = Maze.from_file('../data/labirinto.txt')
    except (FileNotFoundError, ValueError) as e:
        print(f"\nERRO FATAL ao carregar o labirinto: {e}")
        print("Verifique se o arquivo labirinto.txt está na estrutura correta (S, G, #, .)")
    else:
        run_all_searches(maze_instance)
