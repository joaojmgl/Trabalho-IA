# maze_representation.py
from typing import List, Tuple, Dict, Any

# Definições de tipo
Grid = List[List[str]]
Pos = Tuple[int, int]  # (linha, coluna)

class Node:

    def __init__(self, state: Pos, parent: 'Node' = None, action: str = None, 
                 cost: float = 0.0, heuristic: float = 0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost      
        self.heuristic = heuristic
        self.f_score = cost + heuristic # f(n) = g(n) + h(n)
    
    def __lt__(self, other: 'Node') -> bool:
        """Permite comparação entre nós (usado na Fila de Prioridade)."""
        # Comparação padrão para A*
        return self.f_score < other.f_score

class Maze:

    def __init__(self, grid: Grid):
        self.grid = grid
        self.H = len(grid)
        self.W = len(grid[0]) if self.H > 0 else 0
        self.start = self._find('S')
        self.goal = self._find('G')
        
        self.DELTAS = {
            'N': (-1, 0), 
            'S': (1, 0),   
            'O': (0, -1),  
            'L': (0, 1),   
        }

    @staticmethod
    def from_file(filepath: str) -> 'Maze':

        try:
            with open(filepath, 'r') as f:
                grid = [list(line.strip()) for line in f if line.strip()]
            return Maze(grid)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de labirinto não encontrado em: {filepath}")

    def _find(self, ch: str) -> Pos:
        for r in range(self.H):
            for c in range(self.W):
                if self.grid[r][c] == ch:
                    return (r, c)
        raise ValueError(f"Caractere '{ch}' não encontrado no grid")

    def in_bounds(self, p: Pos) -> bool:
        r, c = p
        return 0 <= r < self.H and 0 <= c < self.W

    def passable(self, p: Pos) -> bool:
        r, c = p
        return self.grid[r][c] != '#'

    def actions(self, p: Pos) -> List[str]:
        r, c = p
        valid_actions = []
        for action, (dr, dc) in self.DELTAS.items():
            q = (r + dr, c + dc) 
            if self.in_bounds(q) and self.passable(q):
                valid_actions.append(action)
        return valid_actions

    def result(self, p: Pos, a: str) -> Pos:
        r, c = p
        if a not in self.DELTAS:
            raise ValueError(f"Ação desconhecida: {a}")
            
        dr, dc = self.DELTAS[a]
        q = (r + dr, c + dc)
        
        # A verificação de validade da posição 'q' é mantida por robustez, sem o erro de sintaxe.
        if not (self.in_bounds(q) and self.passable(q)):
             raise ValueError(f"Ação {a} inválida na posição {p}. Resultado fora dos limites ou em parede.")

        return q

    def step_cost(self, p1: Pos, a: str, p2: Pos) -> float:
        return 1.0

    def goal_test(self, p: Pos) -> bool:
        return p == self.goal
