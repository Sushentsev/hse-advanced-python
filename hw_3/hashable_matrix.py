from hw_3.matrix import Matrix


class HashMixin:
    def __hash__(self):
        return sum(map(sum, self.values))


class HashableMatrix(Matrix, HashMixin):
    pass


class MatmulCachedMatrix(HashableMatrix):
    def __init__(self, values):
        super().__init__(values)
        self._cache = {}

    def __matmul__(self, other):
        key = (hash(self), hash(other))
        if key not in self._cache:
            self._cache[key] = super().__matmul__(other)
        return self._cache[key]


if __name__ == "__main__":
    A = MatmulCachedMatrix([
        [1, 2],
        [3, 4]
    ])

    B = MatmulCachedMatrix([
        [5, 6],
        [7, 8]
    ])

    C = MatmulCachedMatrix([
        [2, 1],
        [3, 4]
    ])

    D = MatmulCachedMatrix([
        [5, 6],
        [7, 8]
    ])

    dir = "artifacts/task_3"
    matrices = [A, B, C, D, A @ B, C @ D]
    file_names = ["A.txt", "B.txt", "C.txt", "D.txt", "AB.txt", "CD.txt"]
    for matrix, file_name in zip(matrices, file_names):
        with open(f"{dir}/{file_name}", "w") as file:
            file.write("[\n")
            for row in matrix.values:
                file.write(str(row) + "\n")
            file.write("]\n")

    with open(f"{dir}/hash.txt", "w") as file:
        file.write(f"{hash(A @ B)}, {hash(C @ D)}")
