import unittest

from hw_3.matrix import Matrix


class TestMatrix(unittest.TestCase):
    def test_init_wrong_shapes_1(self):
        values = []
        with self.assertRaises(ValueError):
            Matrix(values)

    def test_init_wrong_shapes_2(self):
        values = [[1, 2, 3], [4, 5]]
        with self.assertRaises(ValueError):
            Matrix(values)

    def test_add_wrong_shapes(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            m1 + m2

    def test_add(self):
        m1 = Matrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix([[5, 6, 7], [8, 9, 10]])
        m3 = m1 + m2
        self.assertListEqual(m3.values, [[6, 8, 10], [12, 14, 16]])

    def test_mul_wrong_shapes(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[4, 5, 6], [7, 8, 9]])
        with self.assertRaises(ValueError):
            m1 * m2

    def test_mul(self):
        m1 = Matrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix([[5, 6, 7], [8, 9, 10]])
        m3 = m1 * m2
        self.assertListEqual(m3.values, [[5, 12, 21], [32, 45, 60]])

    def test_matmul_wrong_shapes(self):
        m1 = Matrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix([[5, 6, 7], [8, 9, 10]])
        with self.assertRaises(ValueError):
            m1 @ m2

    def test_matmul(self):
        m1 = Matrix([
            [2, 3, 1],
            [4, 5, 6]
        ])
        m2 = Matrix([
            [1, 2],
            [3, 4],
            [5, 6]
        ])
        m3 = m1 @ m2
        self.assertListEqual(m3.values, [[16, 22], [49, 64]])


if __name__ == "__main__":
    unittest.main()
