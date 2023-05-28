import json
import queue
import threading
import socket
from test.support import socket_helper

import pytest

from server import server_starter

HOST = "localhost"


def fake_client(
    tmp_queue: queue.Queue,
    host: str,
    port: int,
    urls: list[str],
) -> None:
    timeout = 10
    for url in urls:
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.connect((host, port))
                    client.settimeout(timeout)
                    client.sendall(url.encode())
                    data = client.recv(8192)
                    tmp_queue.put(json.loads(data.decode()))
                    break
            except queue.Empty:
                break
            except TimeoutError:
                break
            except Exception:
                pass


@pytest.mark.parametrize(
    ["workers", "count_words", "urls"],
    [
        [
            2,
            5,
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
            2,
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
def test_server_side(
    mocker,
    workers: int,
    count_words: int,
    urls: list[str],
) -> None:
    port = socket_helper.find_unused_port()
    tmp_queue = queue.Queue()
    responses = [{str(i): i, str(i+1): i+1} for i in range(len(urls))]
    func = mocker.Mock(side_effect=responses)
    server = threading.Thread(
        target=server_starter,
        name="server_thread",
        args=(workers, count_words),
        kwargs={"host": HOST, "port": port, "handler_func": func},
    )
    client = threading.Thread(
        target=fake_client,
        name="fake_client_thread",
        args=(tmp_queue, HOST, port, urls),
    )
    server.start()
    client.start()
    client.join()
    server.join()
    server_requests = []
    calls = [(url, count_words) for url in urls]
    while not tmp_queue.empty():
        server_requests.append(tmp_queue.get())
    assert server_requests == responses
    assert all(
        call._get_call_arguments()[0] == calls[index]
        for index, call in enumerate(func.call_args_list)
    )
