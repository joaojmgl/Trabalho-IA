from typing import Tuple
from math import sqrt, fabs

Pos = Tuple[int, int]  # (linha, coluna)


def h_manhattan(a: Pos, b: Pos) -> float:

    r1, c1 = a
    r2, c2 = b
    return float(fabs(r1 - r2) + fabs(c1 - c2))


def h_euclidiana(a: Pos, b: Pos) -> float:

    r1, c1 = a
    r2, c2 = b
    dist_quadrada = (r1 - r2) ** 2 + (c1 - c2) ** 2
    return sqrt(dist_quadrada)


def h_chebyshev(a: Pos, b: Pos) -> float:

    r1, c1 = a
    r2, c2 = b

    # max(|r_a - r_b|, |c_a - c_b|)
    dist_r = fabs(r1 - r2)
    dist_c = fabs(c1 - c2)

    return float(max(dist_r, dist_c))