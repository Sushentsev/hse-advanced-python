def get_fib(n: int) -> int:
    if n < 0:
        raise ValueError(f"Invalid n: {n}.")

    curr, next_ = 0, 1
    for i in range(n):
        curr, next_ = next_, curr + next_

    return curr
