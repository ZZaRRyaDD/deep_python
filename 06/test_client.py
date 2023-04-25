import json
import random
import queue
import os
import threading
import socket
from collections import Counter

from client import client_starter


def fake_server(tmp_queue: queue.Queue, host: str, port: int) -> None:
    timeout = 10
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(timeout)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        while True:
            try:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(8192)
                    tmp_queue.put(data.decode())
                    send_data = dict(Counter(data).most_common(2))
                    conn.sendall(str(json.dumps(send_data)).encode())
            except TimeoutError:
                break


def test_client_side(tmpdir) -> None:
    tmp_queue = queue.Queue()
    host, port = "localhost", random.randint(1025, 65535)
    server = threading.Thread(
        target=fake_server,
        name="fake_server_thread",
        args=(tmp_queue, host, port),
    )
    server.start()
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
        "https://docs.python.org/3/whatsnew/3.11.html",
    ]
    path = os.path.abspath("/start")
    filename = "file.txt"
    directory = tmpdir.mkdir(path)
    file_path = directory.join(filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines("\n".join(base_urls))
    client = threading.Thread(
        target=client_starter,
        name="client_thread",
        args=(5, file_path),
        kwargs={"host": host, "port": port},
    )
    client.start()
    server.join()
    client.join()
    client_requests = []
    while not tmp_queue.empty():
        client_requests.append(tmp_queue.get())
    assert sorted(client_requests) == sorted(base_urls)
