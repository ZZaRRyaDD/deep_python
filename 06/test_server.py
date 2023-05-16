import json
import queue
import threading
import socket

from server import server_starter
from get_port import get_unused_data


def fake_client(tmp_queue: queue.Queue, host: str, port: int) -> None:
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
    timeout = 10
    for url in base_urls:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                client.settimeout(timeout)
                client.sendall(url.encode())
                data = client.recv(8192)
                tmp_queue.put(json.loads(data.decode()))
        except queue.Empty:
            break
        except TimeoutError:
            break


def test_server_side(mocker) -> None:
    host, port = get_unused_data()
    responses = [{str(i): i, str(i+1): i+1} for i in range(0, 20, 2)]
    mocker.patch("server.handle_url", side_effect=responses)
    server = threading.Thread(
        target=server_starter,
        name="server_thread",
        args=(5, 5),
        kwargs={"host": host, "port": port},
    )
    server.start()
    tmp_queue = queue.Queue()
    client = threading.Thread(
        target=fake_client,
        name="fake_client_thread",
        args=(tmp_queue, host, port),
    )
    client.start()
    client.join()
    server.join()
    server_requests = []
    while not tmp_queue.empty():
        server_requests.append(tmp_queue.get())
    assert server_requests == responses
