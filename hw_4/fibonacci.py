import time
from multiprocessing import Process
from threading import Thread


def get_fib(n):
    if n < 0:
        raise ValueError(f"Invalid n: {n}.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return get_fib(n - 1) + get_fib(n - 2)


def run_synchronously():
    def inner(n, times):
        for _ in range(times):
            get_fib(n)

    return inner


def run_parallel(executor):
    def inner(n, times):
        executors = [executor(target=get_fib, args=(n,)) for _ in range(times)]
        [ex.start() for ex in executors]
        [ex.join() for ex in executors]

    return inner


def eval_time(f, n, times):
    start_time = time.time()
    f(n, times)
    elapsed = time.time() - start_time
    return elapsed


def main():
    n, times = 35, 10

    with open("artifacts/fibonacci.txt", "w") as file:
        file.write(f"n={n}, times={times}\n")
        file.write(f"base: {eval_time(run_synchronously(), n, times):.2f} sec\n")
        file.write(f"threading: {eval_time(run_parallel(Thread), n, times):.2f} sec\n")
        file.write(f"multiprocessing: {eval_time(run_parallel(Process), n, times):.2f} sec\n")


if __name__ == "__main__":
    main()
