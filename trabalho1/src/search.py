# search.py
from typing import Dict, List, Any, Tuple
import time

# Importações dos módulos auxiliares
from maze_representation import Maze, Node, Pos 
from data_structures import Queue, Stack, PriorityQueue
from heuristics import h_manhattan, h_chebyshev

# ====================================================================
# FUNÇÕES AUXILIARES
# ====================================================================

def reconstruct_path(node: Node) -> Tuple[List[Pos], float]:
    path = []
    current = node
    while current is not None:
        path.append(current.state)
        current = current.parent
    
    path.reverse()
    cost = node.cost 
    
    return path, cost

# ====================================================================
# 1. BUSCA EM LARGURA (BFS)
# ====================================================================

def bfs_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()
    start_node = Node(maze.start)
    frontier = Queue()
    frontier.push(start_node)
    explored = {maze.start}
    expanded_positions = []
    solution_node = None
    
    max_memory_usage = 1 
    nodes_expanded = 0
    solution_node = None
    
    while not frontier.is_empty():
        current_memory = len(frontier) + len(explored)
        max_memory_usage = max(max_memory_usage, current_memory)
        
        current_node = frontier.pop()
        
        if maze.goal_test(current_node.state):
            solution_node = current_node
            break
            
        nodes_expanded += 1
        current_pos = current_node.state
        expanded_positions.append(current_pos)  # Rastrear a posição
        
        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            
            if next_pos not in explored:
                new_cost = current_node.cost + maze.step_cost(current_pos, action, next_pos)
                successor_node = Node(state=next_pos, 
                                      parent=current_node, 
                                      action=action, 
                                      cost=new_cost)
                
                frontier.push(successor_node)
                explored.add(next_pos)
    
    end_time = time.time()
    
    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True
        optimal = True
    else:
        path = []; cost = 0.0; success = False; optimal = False

    return {
        'algoritmo': 'BFS (Busca em Largura)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'memoria_maxima': max_memory_usage,
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }

# ====================================================================
# 2. BUSCA EM PROFUNDIDADE (DFS)
# ====================================================================

def dfs_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()
    start_node = Node(maze.start)
    frontier = Stack()
    frontier.push(start_node)
    explored = {maze.start}
    expanded_positions = []
    solution_node = None
    
    max_memory_usage = 1 
    nodes_expanded = 0
    solution_node = None
    
    while not frontier.is_empty():
        current_memory = len(frontier) + len(explored)
        max_memory_usage = max(max_memory_usage, current_memory)
        
        current_node = frontier.pop()
        
        if maze.goal_test(current_node.state):
            solution_node = current_node
            break
            
        nodes_expanded += 1
        current_pos = current_node.state
        expanded_positions.append(current_pos)  # Rastrear a posição
        
        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            
            if next_pos not in explored:
                new_cost = current_node.cost + maze.step_cost(current_pos, action, next_pos)
                successor_node = Node(state=next_pos, 
                                      parent=current_node, 
                                      action=action, 
                                      cost=new_cost)
                
                frontier.push(successor_node)
                explored.add(next_pos)
    
    end_time = time.time()
    
    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True; optimal = False
    else:
        path = []; cost = 0.0; success = False; optimal = False

    return {
        'algoritmo': 'DFS (Busca em Profundidade)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'memoria_maxima': max_memory_usage,
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }

# ====================================================================
# 3. BUSCA DE CUSTO UNIFORME (UCS)
# ====================================================================

def ucs_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()
    start_node = Node(maze.start, cost=0.0)
    frontier = PriorityQueue()
    frontier.push(start_node.cost, start_node)
    g_scores = {maze.start: 0.0}
    expanded_positions = []
    solution_node = None
    
    max_memory_usage = 1 
    nodes_expanded = 0
    solution_node = None
    
    while not frontier.is_empty():
        current_memory = len(frontier) + len(g_scores)
        max_memory_usage = max(max_memory_usage, current_memory)
        
        current_node = frontier.pop()
        current_pos = current_node.state
        
        if maze.goal_test(current_pos):
            solution_node = current_node
            break
            
        nodes_expanded += 1
        expanded_positions.append(current_pos)
        
        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            step_cost = maze.step_cost(current_pos, action, next_pos)
            new_cost = current_node.cost + step_cost
            
            if next_pos not in g_scores or new_cost < g_scores[next_pos]:
                g_scores[next_pos] = new_cost
                
                successor_node = Node(state=next_pos, parent=current_node, 
                                      action=action, cost=new_cost)
                
                frontier.push(successor_node.cost, successor_node)
    
    end_time = time.time()
    
    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True; optimal = True
    else:
        path = []; cost = 0.0; success = False; optimal = False

    return {
        'algoritmo': 'UCS (Custo Uniforme)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'memoria_maxima': max_memory_usage,
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }

# ====================================================================
# 4. BUSCA GULOSA (GREEDY BEST-FIRST SEARCH)
# ====================================================================

def greedy_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()
    h_start = h_manhattan(maze.start, maze.goal)
    start_node = Node(maze.start, cost=0.0, heuristic=h_start)
    frontier = PriorityQueue()
    frontier.push(start_node.heuristic, start_node) # Prioridade: h(n)
    explored = {maze.start}
    expanded_positions = []
    solution_node = None
    
    max_memory_usage = 1 
    nodes_expanded = 0
    solution_node = None
    
    while not frontier.is_empty():
        current_memory = len(frontier) + len(explored)
        max_memory_usage = max(max_memory_usage, current_memory)
        
        current_node = frontier.pop()
        current_pos = current_node.state
        
        if maze.goal_test(current_pos):
            solution_node = current_node
            break
            
        nodes_expanded += 1
        expanded_positions.append(current_pos)  # Rastrear a posição
        
        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            
            if next_pos not in explored:
                step_cost = maze.step_cost(current_pos, action, next_pos)
                new_cost = current_node.cost + step_cost 
                new_h = h_manhattan(next_pos, maze.goal)
                
                successor_node = Node(state=next_pos, parent=current_node, 
                                      action=action, cost=new_cost, heuristic=new_h)
                
                frontier.push(successor_node.heuristic, successor_node)
                explored.add(next_pos)
    
    end_time = time.time()
    
    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True; optimal = False
    else:
        path = []; cost = 0.0; success = False; optimal = False

    return {
        'algoritmo': 'Busca Gulosa (Greedy)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'memoria_maxima': max_memory_usage,
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }

# ====================================================================
# 5. BUSCA A* (A-STAR SEARCH)
# ====================================================================

def astar_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()
    h_start = h_manhattan(maze.start, maze.goal)
    start_node = Node(maze.start, cost=0.0, heuristic=h_start)
    frontier = PriorityQueue()
    frontier.push(start_node.f_score, start_node) # Prioridade: f(n)
    g_scores = {maze.start: 0.0}
    expanded_positions = []
    solution_node = None
    
    max_memory_usage = 1 
    nodes_expanded = 0
    solution_node = None
    
    while not frontier.is_empty():
        current_memory = len(frontier) + len(g_scores)
        max_memory_usage = max(max_memory_usage, current_memory)
        
        current_node = frontier.pop()
        current_pos = current_node.state
        
        if maze.goal_test(current_pos):
            solution_node = current_node
            break
            
        nodes_expanded += 1
        expanded_positions.append(current_pos)  # Rastrear a posição
        
        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            step_cost = maze.step_cost(current_pos, action, next_pos)
            new_cost = current_node.cost + step_cost

            if next_pos not in g_scores or new_cost < g_scores[next_pos]:
                g_scores[next_pos] = new_cost
                
                new_h = h_manhattan(next_pos, maze.goal)
                
                successor_node = Node(state=next_pos, parent=current_node, 
                                      action=action, cost=new_cost, heuristic=new_h)

                frontier.push(successor_node.f_score, successor_node)
    
    end_time = time.time()
    
    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True; optimal = True
    else:
        path = []; cost = 0.0; success = False; optimal = False

    return {
        'algoritmo': 'A* (A-Star)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'memoria_maxima': max_memory_usage,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }


# ====================================================================
# 6. BUSCA GULOSA COM CHEBYSHEV
# ====================================================================

def greedy_chebyshev_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()

    # A heurística usada é h_chebyshev
    h_func = h_chebyshev

    h_start = h_func(maze.start, maze.goal)
    start_node = Node(maze.start, cost=0.0, heuristic=h_start)
    frontier = PriorityQueue()
    frontier.push(start_node.heuristic, start_node)
    explored = {maze.start}
    expanded_positions = []
    solution_node = None

    max_memory_usage = 1
    nodes_expanded = 0
    solution_node = None

    while not frontier.is_empty():
        current_memory = len(frontier) + len(explored)
        max_memory_usage = max(max_memory_usage, current_memory)
        current_node = frontier.pop()
        current_pos = current_node.state

        if maze.goal_test(current_pos):
            solution_node = current_node
            break

        nodes_expanded += 1
        expanded_positions.append(current_pos)  # Rastrear a posição

        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)

            if next_pos not in explored:
                step_cost = maze.step_cost(current_pos, action, next_pos)
                new_cost = current_node.cost + step_cost
                new_h = h_func(next_pos, maze.goal)

                successor_node = Node(state=next_pos, parent=current_node,
                                      action=action, cost=new_cost, heuristic=new_h)

                frontier.push(successor_node.heuristic, successor_node)
                explored.add(next_pos)

    end_time = time.time()

    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True;
        optimal = False
    else:
        path = [];
        cost = 0.0;
        success = False;
        optimal = False

    return {
        'algoritmo': 'Busca Gulosa (Chebyshev)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'memoria_maxima': max_memory_usage,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }


# ====================================================================
# 7. BUSCA A* COM CHEBYSHEV
# ====================================================================

def astar_chebyshev_search(maze: Maze) -> Dict[str, Any]:
    start_time = time.time()

    # A heurística usada é h_chebyshev
    h_func = h_chebyshev

    h_start = h_func(maze.start, maze.goal)
    start_node = Node(maze.start, cost=0.0, heuristic=h_start)
    frontier = PriorityQueue()
    frontier.push(start_node.f_score, start_node)  # Prioridade: f(n)
    g_scores = {maze.start: 0.0}
    expanded_positions = []
    solution_node = None

    max_memory_usage = 1
    nodes_expanded = 0
    solution_node = None

    while not frontier.is_empty():
        current_memory = len(frontier) + len(g_scores)
        max_memory_usage = max(max_memory_usage, current_memory)
        current_node = frontier.pop()
        current_pos = current_node.state

        if maze.goal_test(current_pos):
            solution_node = current_node
            break

        nodes_expanded += 1
        expanded_positions.append(current_pos)  # Rastrear a posição

        for action in maze.actions(current_pos):
            next_pos = maze.result(current_pos, action)
            step_cost = maze.step_cost(current_pos, action, next_pos)
            new_cost = current_node.cost + step_cost

            if next_pos not in g_scores or new_cost < g_scores[next_pos]:
                g_scores[next_pos] = new_cost
                new_h = h_func(next_pos, maze.goal)

                successor_node = Node(state=next_pos, parent=current_node,
                                      action=action, cost=new_cost, heuristic=new_h)

                frontier.push(successor_node.f_score, successor_node)

    end_time = time.time()

    if solution_node:
        path, cost = reconstruct_path(solution_node)
        success = True;
        optimal = True
    else:
        path = [];
        cost = 0.0;
        success = False;
        optimal = False

    return {
        'algoritmo': 'A* (Chebyshev)',
        'sucesso': success, 'custo_total': cost, 'caminho': path,
        'nos_expandidos': nodes_expanded,
        'nos_expandidos_posicoes': expanded_positions,  # NOVO RETORNO
        'memoria_maxima': max_memory_usage,
        'tempo_execucao': end_time - start_time, 'optimalidade': optimal,
        'completude': success
    }