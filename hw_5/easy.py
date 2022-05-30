import asyncio
import time
from functools import wraps
from os.path import join
from pathlib import Path
from aiohttp import ClientSession
import requests


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"Elapsed time: {elapsed:.2f} seconds.")
        return res

    return wrapper


URL = "https://picsum.photos/200/300"


def create_dir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)


def download_img_sync(url, session, save_path):
    with session.get(url) as response:
        with open(save_path, "wb") as file:
            file.write(response.content)


def download_all_sync(n, save_dir):
    create_dir(save_dir)

    with requests.Session() as session:
        for i in range(n):
            save_path = join(save_dir, f"{i}.jpeg")
            download_img_sync(URL, session, save_path)


async def download_img_async(url, session, save_path):
    async with session.get(url, ssl=False) as response:
        r = await response.read()
        with open(save_path, "wb") as f:
            f.write(r)


async def download_all_async(n, save_dir):
    create_dir(save_dir)

    async with ClientSession(trust_env=True) as session:
        tasks = []
        for i in range(n):
            save_path = join(save_dir, f"{i}.jpeg")
            task = asyncio.create_task(download_img_async(URL, session, save_path))
            tasks.append(task)

        return await asyncio.gather(*tasks)


@timeit
def download(n, save_dir, sync):
    if sync:
        download_all_sync(n, save_dir)
    else:
        asyncio.run(download_all_async(n, save_dir))


if __name__ == "__main__":
    N = 500
    download(N, "./artifacts/sync/", sync=True)
    download(N, "./artifacts/async/", sync=False)

# Sync elapsed time: 66.29 seconds.
# Async elapsed time: 1.77 seconds.
