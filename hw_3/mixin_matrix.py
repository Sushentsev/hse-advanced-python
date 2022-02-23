import numpy as np


class ArithmeticMixin(np.lib.mixins.NDArrayOperatorsMixin):
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        for input in inputs:
            if not isinstance(input, type(self)):
                return NotImplemented
        inputs = (input.values for input in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return type(self)(result)


class WriteToFileMixin:
    def write_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write(str(self))


class StrMixin:
    def __str__(self):
        out = ""
        for row in self.values:
            out += "\t".join(map(str, row)) + "\n"
        return out


class GetterMixin:
    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self.__dict__["_" + item]


class ArrayLike:
    def __init__(self, values):
        self._values = np.asarray(values)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, x):
        self._values = x


class Matrix(ArrayLike, ArithmeticMixin, StrMixin, WriteToFileMixin):
    pass


if __name__ == '__main__':
    np.random.seed(0)
    matrix_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix_2 = Matrix(np.random.randint(0, 10, (10, 10)))

    dir = "artifacts/task_2"
    ops = [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: x @ y]
    files = ["matrix+.txt", "matrix*.txt", "matrix@.txt"]

    for op, file_name in zip(ops, files):
        op(matrix_1, matrix_2).write_to_file(f"{dir}/{file_name}")
