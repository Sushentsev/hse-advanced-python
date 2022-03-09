import math
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


class Logger:
    def __init__(self):
        self.queue = multiprocessing.Manager().Queue()

    def log(self, msg):
        self.queue.put(msg)

    def save(self, path):
        with open(path, "w") as file:
            while not self.queue.empty():
                file.write(self.queue.get() + "\n")


# def log(_func=None, my_logger=None):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # logger_ = my_logger
#             # if logger_ is None:
#             #     logger_ = Logger()
#             # logger_.log(f"Function call with params {args} and {kwargs}")
#             logger.log(f"Function call with params {args} and {kwargs}")
#             return func(*args, *kwargs)
#
#         return wrapper
#
#     return decorator


# def log(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         logger.log(f"Function call with params {args} and {kwargs}")
#         return func(*args, *kwargs)
#
#     return wrapper


def eval_step(f, a, i, step, logger):
    logger.log(f"Function call on {i} iteration")
    out = f(a + i * step) * step
    return out


def integrate(f, a, b, *, n_jobs=1, n_iter=1_000, executor, logger):
    with executor(max_workers=n_jobs) as executor:
        step = (b - a) / n_iter
        args = [(f, a, i, step) for i in range(n_iter)]
        futures = []
        for (f, a, i, step) in args:
            futures.append(executor.submit(eval_step, f, a, i, step, logger))
        res = sum(future.result() for future in as_completed(futures))
        return res


def eval_time(f, *args, **kwargs):
    start_time = time.time()
    f(*args, **kwargs)
    elapsed = time.time() - start_time
    return elapsed


def main():
    logger = Logger()
    with open("artifacts/integrate_time.txt", "w") as file:
        for n_cpu in range(1, 16 + 1):
            executors = {"thread executor": ThreadPoolExecutor, "process executor": ProcessPoolExecutor}
            for (ex_name, executor) in executors.items():
                elapsed = eval_time(integrate, math.cos, 0, math.pi / 2,
                                    n_jobs=n_cpu, n_iter=1_000, executor=executor, logger=logger)
                file.write(f"Executor '{ex_name}' with {n_cpu} jobs: {elapsed:.4f} sec\n")

    logger.save("artifacts/integrate_logs.txt")


if __name__ == "__main__":
    main()
