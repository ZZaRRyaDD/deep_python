import asyncio
import os

import pytest

from fetcher import server_starter, worker_task


@pytest.mark.asyncio
async def test_async_server(mocker, tmpdir, capsys):
    base_urls = [
        "https://shikimori.me/",
        "https://mail.yandex.ru/",
        "https://www.youtube.com/",
        "https://stepik.org/catalog",
        "https://github.com/PC-Nazarka",
        "https://gitlab.com/PC-Nazarka",
        "https://dzen.ru/",
        "https://ya.ru/",
        "https://krasnoyarsk.hh.ru/",
        "https://ru.wikipedia.org/wiki/Python",
    ]
    path = os.path.abspath("/start")
    filename = "file.txt"
    directory = tmpdir.mkdir(path)
    file_path = directory.join(filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(base_urls))
    responses = [{str(i): i, str(i+1): i+1} for i in range(0, 20, 2)]
    mocker.patch('fetcher.handle_url', side_effect=responses)
    await server_starter(5, file_path)
    captured = capsys.readouterr()
    result = "".join(
        [
            f"{url}: {response}"
            for url, response in zip(base_urls, responses)
        ]
    )
    assert captured.out.replace("\n", "") == result


@pytest.mark.asyncio
async def test_async_server_with_one_worker(mocker, tmpdir, capsys):
    base_urls = [
        "https://shikimori.me/",
        "https://mail.yandex.ru/",
        "https://www.youtube.com/",
        "https://stepik.org/catalog",
        "https://github.com/PC-Nazarka",
        "https://gitlab.com/PC-Nazarka",
        "https://dzen.ru/",
        "https://ya.ru/",
        "https://krasnoyarsk.hh.ru/",
        "https://ru.wikipedia.org/wiki/Python",
    ]
    path = os.path.abspath("/start")
    filename = "file.txt"
    directory = tmpdir.mkdir(path)
    file_path = directory.join(filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(base_urls))
    responses = [{str(i): i, str(i+1): i+1} for i in range(0, 20, 2)]
    mocker.patch('fetcher.handle_url', side_effect=responses)
    await server_starter(1, file_path)
    captured = capsys.readouterr()
    result = "".join(
        [
            f"{url}: {response}"
            for url, response in zip(base_urls, responses)
        ]
    )
    assert captured.out.replace("\n", "") == result


@pytest.mark.asyncio
async def test_worker(mocker, tmpdir, capsys):
    base_urls = [
        "https://shikimori.me/",
        "https://mail.yandex.ru/",
        "https://www.youtube.com/",
        "https://stepik.org/catalog",
        "https://github.com/PC-Nazarka",
        "https://gitlab.com/PC-Nazarka",
        "https://dzen.ru/",
        "https://ya.ru/",
        "https://krasnoyarsk.hh.ru/",
        "https://ru.wikipedia.org/wiki/Python",
    ]
    path = os.path.abspath("/start")
    filename = "file.txt"
    directory = tmpdir.mkdir(path)
    file_path = directory.join(filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(base_urls))
    responses = [{str(i): i, str(i+1): i+1} for i in range(0, 20, 2)]
    mocker.patch('fetcher.handle_url', side_effect=responses)
    main_queue = asyncio.Queue(maxsize=1)
    workers = [
        asyncio.create_task(worker_task(main_queue))
    ]
    with open(file_path, "r", encoding="utf-8") as file:
        while line := file.readline():
            await main_queue.put(line.replace("\n", ""))
    await main_queue.join()
    for worker in workers:
        worker.cancel()
    captured = capsys.readouterr()
    result = "".join(
        [
            f"{url}: {response}"
            for url, response in zip(base_urls, responses)
        ]
    )
    assert captured.out.replace("\n", "") == result
