from typing import List


def get_fib(n: int) -> List[int]:
    if n <= 0:
        raise ValueError(f"Invalid n: {n}.")

    if n == 1:
        return [0]

    values = [0, 1]
    for i in range(n - 2):
        values.append(values[-1] + values[-2])

    return values
