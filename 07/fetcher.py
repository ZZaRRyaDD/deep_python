import argparse
import asyncio
from collections import Counter

import aiohttp


async def handle_url(
    url: str,
    session: aiohttp.ClientSession,
    most_common: int = 5,
) -> dict:
    async with session.get(url) as response:
        data = await response.text()
        for symbol in ["\n", "\\", "<", ">"]:
            data = data.replace(symbol, "")
        data = data.split()
        return dict(Counter(data).most_common(most_common))


async def worker_task(queue: asyncio.Queue) -> None:
    async with aiohttp.ClientSession() as session:
        while True:
            url = await queue.get()
            data = await handle_url(url, session)
            queue.task_done()
            print(f"{url}: {data}\n")


async def server_starter(count_workers: int, path: str) -> None:
    main_queue = asyncio.Queue()
    workers = [
        asyncio.create_task(worker_task(main_queue))
        for _ in range(count_workers)
    ]
    with open(path, "r", encoding="utf-8") as file:
        while line := file.readline():
            await main_queue.put(line.replace("\n", ""))
    await main_queue.join()
    for worker in workers:
        worker.cancel()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Сбор параметров для обкачки урлов",
    )
    parser.add_argument(
        "count_workers",
        type=int,
        help="Количество воркеров",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Путь к файлу",
    )
    args = parser.parse_args()
    asyncio.run(server_starter(args.count_workers, args.path))


if __name__ == "__main__":
    main()
