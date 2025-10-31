from typing import List, Iterable, Tuple
import random

# Type Definitions
N = 8  # Tamanho do tabuleiro
Board = List[int]  # board[coluna] = linha (0 a 7)
Move = Tuple[int, int]  # (coluna, nova_linha)


class EightQueensProblem:
    """
    Representação do estado, transições e função de avaliação para o Problema das 8 Rainhas.
    """

    def __init__(self, size: int = N):
        self.size = size
        # Opcional: Definir uma semente fixa para reprodutibilidade das boards iniciais
        # random.seed(42)

    def initial_board(self) -> Board:
        """
        Gera um estado inicial aleatório.
        """
        return [random.randint(0, self.size - 1) for _ in range(self.size)]

    def conflicts(self, board: Board) -> int:
        """
        Função de avaliação: calcula o número de pares de rainhas em conflito[cite: 90].
        Conflito: linha (horizontal) ou diagonal.
        """
        conflicts = 0

        # Compara cada par de rainhas
        for i in range(self.size):
            for j in range(i + 1, self.size):

                # Conflito de Linha (Horizontal)
                if board[i] == board[j]:
                    conflicts += 1

                # Conflito de Diagonal (|row_i - row_j| == |col_i - col_j|)
                row_diff = abs(board[i] - board[j])
                col_diff = abs(i - j)

                if row_diff == col_diff:
                    conflicts += 1

        return conflicts

    def neighbors(self, board: Board) -> Iterable[Tuple[Move, Board]]:
        """
        Gera todos os estados vizinhos possíveis[cite: 91].
        O operador de vizinhança é: mover uma rainha em sua coluna para outra linha.
        """
        for c in range(self.size):
            current_row = board[c]

            # Tenta todas as outras linhas (r) na coluna c
            for r in range(self.size):
                if r != current_row:
                    move = (c, r)
                    new_board = self.apply_move(board, move)
                    yield (move, new_board)

    def apply_move(self, board: Board, mv: Move) -> Board:
        """
        Retorna um novo tabuleiro após aplicar o movimento mv: (coluna, nova_linha).
        """
        c, r = mv
        new_board = board.copy()
        new_board[c] = r
        return new_board