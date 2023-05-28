import json
import queue
import os
import threading
import socket
from collections import Counter
from test.support import socket_helper

import pytest

from client import client_starter

HOST = "localhost"


def fake_server(
    get_urls: queue.Queue,
    sended_data: queue.Queue,
    host: str,
    port: int,
) -> None:
    timeout = 10
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(timeout)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        while True:
            try:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(8192)
                    get_data = data.decode().replace("\n", "")
                    get_urls.put(get_data)
                    send_data = dict(Counter(get_data).most_common(2))
                    sended_data.put(send_data)
                    conn.sendall(str(json.dumps(send_data)).encode())
            except TimeoutError:
                break


@pytest.mark.parametrize(
    ["count_threads", "urls"],
    [
        [
            2,
            [
                "https://shikimori.me/",
                "https://mail.yandex.ru/",
                "https://stepik.org/catalog",
                "https://dzen.ru/",
                "https://ya.ru/",
                "https://krasnoyarsk.hh.ru/",
            ],
        ],
        [
            7,
            [
                "https://shikimori.me/",
                "https://mail.yandex.ru/",
                "https://stepik.org/catalog",
                "https://krasnoyarsk.hh.ru/",
            ],
        ],
        [
            10,
            [
                "https://shikimori.me/",
                "https://mail.yandex.ru/",
                "https://www.youtube.com/",
                "https://stepik.org/catalog",
                "https://github.com/PC-Nazarka",
                "https://gitlab.com/PC-Nazarka",
                "https://dzen.ru/",
                "https://ya.ru/",
                "https://krasnoyarsk.hh.ru/",
                "https://docs.python.org/3/whatsnew/3.11.html",
            ],
        ],
    ],
)
def test_client_side(
    tmpdir,
    capsys,
    count_threads: int,
    urls: list[str],
) -> None:
    get_urls = queue.Queue()
    send_data = queue.Queue()
    port = socket_helper.find_unused_port()
    server = threading.Thread(
        target=fake_server,
        name="fake_server_thread",
        args=(get_urls, send_data, HOST, port),
    )
    server.start()
    path = os.path.abspath("/start")
    filename = "file.txt"
    directory = tmpdir.mkdir(path)
    file_path = directory.join(filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(urls))
    client = threading.Thread(
        target=client_starter,
        name="client_thread",
        args=(count_threads, file_path),
        kwargs={"host": HOST, "port": port},
    )
    client.start()
    server.join()
    client.join()
    captured = capsys.readouterr()
    client_requests = []
    while not get_urls.empty():
        client_requests.append(get_urls.get())
    assert sorted(client_requests) == sorted(urls)

    sended_values = []
    while not send_data.empty():
        sended_values.append(send_data.get())
    assert sorted([
        line
        for line in map(lambda x: x[x.find("{"):], captured.out.split("\n"))
        if line
    ]) == sorted(list(map(str, sended_values)))
