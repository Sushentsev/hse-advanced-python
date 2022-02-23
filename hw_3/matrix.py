from typing import List, Any, Tuple, Callable

import numpy as np


class Matrix:
    def __init__(self, values):
        n_rows = len(values)
        if n_rows == 0:
            raise ValueError("Matrix must be non-empty")

        n_cols = len(values[0])
        if not all(len(row) == n_cols for row in values):
            raise ValueError("All rows must have the same length")

        self._values = values
        self._shape = (n_rows, n_cols)

    def _component_operation(self, other: "Matrix", func: Callable[[Any, Any], Any]) -> "Matrix":
        if not isinstance(other, Matrix):
            raise TypeError("Unsupported operand type(s)")

        if self.shape != other.shape:
            raise ValueError(f"Matrices have incorrect shapes: {self.shape} and {other.shape}")

        values = []
        for row_1, row_2 in zip(self.values, other.values):
            out = list(map(lambda pair: func(*pair), zip(row_1, row_2)))
            values.append(out)

        return type(self)(values)

    def _matrix_operation(self, other: "Matrix", func: Callable[[Any, Any], Any]) -> "Matrix":
        if not isinstance(other, Matrix):
            raise TypeError("Unsupported operand type(s)")

        rows_A, cols_A = self.shape
        rows_B, cols_B = other.shape
        if cols_A != rows_B:
            raise ValueError(f"Matrices have incorrect shapes: {self.shape} and {other.shape}")

        values = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    values[i][j] += func(self.values[i][k], other.values[k][j])

        return type(self)(values)

    def __add__(self, other: "Matrix") -> "Matrix":
        return self._component_operation(other, lambda x, y: x + y)

    def __mul__(self, other: "Matrix") -> "Matrix":
        return self._component_operation(other, lambda x, y: x * y)

    def __matmul__(self, other: "Matrix") -> "Matrix":
        return self._matrix_operation(other, lambda x, y: x * y)

    @property
    def values(self) -> List[List[Any]]:
        return self._values

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape


if __name__ == "__main__":
    np.random.seed(0)
    matrix_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix_2 = Matrix(np.random.randint(0, 10, (10, 10)))

    dir = "artifacts/task_1"
    ops = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: x @ y]
    files = ["matrix+.txt", "matrix*.txt", "matrix@.txt"]

    for op, file_name in zip(ops, files):
        with open(f"{dir}/{file_name}", "w") as file:
            matrix = op(matrix_1, matrix_2)
            file.write("[\n")
            for row in matrix.values:
                file.write(str(row) + "\n")
            file.write("]\n")
